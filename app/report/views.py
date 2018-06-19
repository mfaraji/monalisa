from flask import render_template, g, request, flash
from flask_login import login_required
from ..report import report_b
from .models import Report
from .forms import ReportForm


raw_query = """
With #esStg as (
Select
es.EventKey
,es.SessionKey
,es.PstDay
,es.PstTime
,es.AffiliateKey
,es.ReferrerTypeKey
,es.ReferrerDomain
,es.ReferrerKeyword
,es.Keyword
,es.PageNumber
,es.UsageCount as Searches
From bdm.ViewSearchEvents es
join (Select AffiliateKey, lower(Contract) as Contract, OldCobrandId From bdm.Affiliate where lower(Contract) in {contracts}) aff on es.AffiliateKey = aff.AffiliateKey
join bdm.TimeInDay tid on tid.TimeKey = es.PstTime
Where
es.PstDay between  '{from_date}' and  '{to_date}'
and es.IsCrawler = 0
and es.IsInternalIpAddress = 0
and es.IsSpamView = 0
and es.IsTqFiltered = 0
and es.IsRobot = 0
LIMIT 100
),
#esStg2 as (
Select
es.*
,eb.BrowserKey
,eb.OsKey
From bdm.EventSessionBrowser eb
join #esStg es on es.EventKey = eb.EventKey and es.PstDay = eb.PstDay
Where
eb.PstDay between '{from_date}' and  '{to_date}'
),

/* ADD GEOGRAPHY DATA TO SEARCHES */
#esStg3 as (
Select
es.*
,eg.GeographyKey
,eg.InternetConnectionKey
From bdm.EventGeography eg
join #esStg2 es on es.EventKey = eg.EventKey and es.PstDay = eg.PstDay
Where
eg.PstDay between '{from_date}' and  '{to_date}'
),


#esStg4 as (
Select
es.*
,ip.Ip
From #esStg3 es
join bdm.EventSessionIp ip on es.EventKey = ip.EventKey and es.PstDay = ip.PstDay
Where
ip.PstDay between '{from_date}' and  '{to_date}'
),

#coTmp as (
Select ClickableObjectKey From bdm.ClickableObject Where ClickableObjectType in ('External-Engines', 'QI')
),
#ecStg as (
Select
ec.ParentEventKey
,Sum(case when ec.IsPaid = 0 then ec.usageCount else 0 END) as NonPaidClicks
,Sum(case when ec.ispaid = 1 then ec.usageCount else 0 END) as PaidClicks
From bdm.ViewSRClickEvents ec
join #esStg4 es on es.EventKey = ec.ParentEventKey
join (Select AffiliateKey, lower(Contract) as Contract, OldCobrandId From bdm.Affiliate where lower(Contract) in {contracts}) aff on ec.AffiliateKey = aff.AffiliateKey
join #coTmp co on ec.ClickableObjectKey = co.ClickableObjectKey
Where
ec.PstDay between '{from_date}' and  '{to_date}'
Group by
ec.ParentEventKey
),

#geoTmp as (
Select t.GeographyKey, t.Country
From bdm.Geography t
join #esStg4 f on t.GeographyKey = f.GeographyKey
Group by t.GeographyKey,t.Country
)

Select
f.PstDay as Date
,aff.OldCobrandId as Cobrand
,rt.ReferrerType
,f.ReferrerDomain
,f.ReferrerKeyword
,f.IP as IPAddress
,br.BrowserName as Browser
,cntry.Country
,sum(case when f.PageNumber = 1 Then f.Searches else 0 End) As Searches
,sum(IsNull(ec.PaidClicks,0)) as PaidClicks
,f.Keyword
From #esStg4 f
join (Select AffiliateKey, lower(Contract) as Contract, OldCobrandId From bdm.Affiliate where lower(Contract) in {contracts}) aff on f.AffiliateKey = aff.AffiliateKey
join bdm.Browser br on f.BrowserKey = br.BrowserKey
join bdm.ReferrerType rt on f.ReferrerTypeKey = rt.ReferrerTypeKey
left join #ecStg ec on f.EventKey = ec.ParentEventKey
join #geoTmp cntry on cntry.GeographyKey = f.GeographyKey
Group by
f.PstDay
,aff.OldCobrandId
,rt.ReferrerType
,f.ReferrerDomain
,f.ReferrerKeyword
,f.IP
,br.BrowserName
,cntry.Country
,f.Keyword
"""

@report_b.route('/', methods=['GET', 'POST'])
@login_required
def list():

    from app.database import DataTable
    datatable = DataTable(
        model=Report,
        columns=[],
        filterable=[],
        sortable=[Report.name, Report.created_ts, Report.last_run],
        searchable=[Report.name],
        limits=[25, 50, 100],
        request=request
    )

    if g.pjax:
        return render_template('reports.html', datatable=datatable)

    return render_template('reports_list.html', datatable=datatable)


@report_b.route('/run/<int:id>', methods=['GET', 'POST'])
@login_required
def run(id):
    report = Report.query.filter_by(id=id).first_or_404()
    form = ReportForm(obj=report)
    if form.validate_on_submit():
        print(create_query(form.data))
        flash(
            'Report {report} Created'.format(report=report.name),
            'success'
        )
    return render_template('report.html', form=form, report=report)


def create_query(params):
    parameters = {}
    parameters['from_date'] = str(params['from_date'])
    parameters['to_date'] = str(params['to_date'])
    parameters['contracts'] = str(tuple(params['contracts'] + ['test']))
    return raw_query.format(**parameters)

