from orator import DatabaseManager
from decimal import Decimal
from config.config import JConfig

config = JConfig()
db_config = {
    config.get('main', 'driver', "mysql"): {
        'driver': config.get('main', 'driver', "mysql"),
        'host': config.get('main', 'mysql_host', "127.0.0.1"),
        'database': config.get('main', 'mysql_database', ""),
        'user': config.get('main', 'mysql_user', "root"),
        'password': config.get('main', 'mysql_password', "123456"),
        "port": config.getint('main', 'mysql_port', "3306")
    }
}
db = DatabaseManager(db_config)


class HomepageStatisticsServices():
    @staticmethod
    def statistics(params: dict = None):
        deal_orders = db.table('enroll_enroll').where_in('enroll_status_code', [80, 668]).count()
        number_escorters = db.table(db.raw(f"role_user_to_role as r1")).left_join(db.raw(f"role_role as r2"),
                                                                                  'r1.role_id',
                                                                                  '=', 'r2.id').where_in('role',
                                                                                                         ['BX-WORKER',
                                                                                                          'CASUAL_WORKER']).count()
        bid_winning_amount = db.table('thread').sum('field_2')

        statistics = {
            'deal_orders': deal_orders,
            'number_escorters': number_escorters,
            'bid_winning_amount': bid_winning_amount if bid_winning_amount else Decimal('0.0')
        }
        return statistics, None
