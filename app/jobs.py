from app.extensions import rq

from sqlalchemy import create_engine

en = create_engine('redshift+psycopg2://rs_adhoc_usr:R5adL0cK@insp-dw-prod01.cogvbioiyusk.us-west-2.redshift.amazonaws.com:5439/bdm')


@rq.job
def execute_query(query):
    """Sends a registratiion email to the given uid."""
    result = en.execute(query)
    r = [r for r in result]
    print(r)
    return r
