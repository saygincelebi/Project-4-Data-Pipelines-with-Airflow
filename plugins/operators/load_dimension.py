from airflow.hooks.postgres_hook import PostgresHook
from airflow.models import BaseOperator
from airflow.utils.decorators import apply_defaults

class LoadDimensionOperator(BaseOperator):

    ui_color = '#80BD9E'
    truncate_stmt = """
        TRUNCATE TABLE {table}
    """
    insert_into_stmt = """
        INSERT INTO {table} 
        {select_query}
    """

    @apply_defaults
    def __init__(self,
                 # Operator params are defined here
                 redshift_conn_id,
                 table,
                 select_query,
                 truncate_table=True,
                 *args, **kwargs):

        super(LoadDimensionOperator, self).__init__(*args, **kwargs)

        self.redshift_conn_id = redshift_conn_id
        self.table = table
        self.select_query = select_query
        self.truncate_table = truncate_table

    def execute(self, context):
        redshift = PostgresHook(postgres_conn_id=self.redshift_conn_id)
        
        # Perform truncate
        if self.truncate_table:
            self.log.info("Truncating dim table..")
            redshift.run(LoadDimensionOperator.truncate_stmt.format(
                table=self.table
            ))
        # Perform insert
        self.log.info("Inserting into dim table..")
        redshift.run(LoadDimensionOperator.insert_into_stmt.format(
            table=self.table,
            select_query=self.select_query
        ))