from pathlib import Path
import os

root_dir = str(Path(__file__).parent.parent)

database: str = 'database.db'
table_name: str = 'intercoms'

report_dir_path = os.path.join(os.sep, root_dir, 'GUI_testrun', 'static')

db_schema_path = os.path.join(os.sep, root_dir, 'GUI_testrun', 'schema.sql')

polygon_devices: list[tuple] = [
    (1, '10.27.52.108', 'Base', '2n', 'beta', '10.27.58.82'),
    (2, '10.27.52.109', 'Base', '2n', 'beta', '10.27.58.82'),
    (3, '10.27.52.121', 'Vario', '2n', 'beta', '10.27.58.82'),
    (4, '10.27.52.111', 'Vario', '2n', 'beta', '10.27.58.82'),
    (5, '10.27.52.107', 'Uni', '2n', 'beta', '10.27.58.82'),
    (6, '10.27.52.115', 'Solo', '2n', 'beta', '10.27.58.82'),
    (7, '10.27.52.102', 'AU', '2n', 'beta', '10.27.58.82'),
    (8, '10.27.52.116', 'AU 2.0', '2n', 'beta', '10.27.58.82'),
    (9, '10.27.52.114', 'Safety', '2n', 'beta', '10.27.58.82'),
    (10, '10.27.52.104', 'Video Kit', '2n', 'beta', '10.27.58.82'),
    (11, '10.27.52.105', 'Audio Kit', '2n', 'beta', '10.27.58.82'),
    (12, '10.27.52.110', 'Verso', '2n', 'beta', '10.27.58.82'),
    (13, '10.27.52.101', 'Verso', '2n', 'beta', '10.27.58.82'),
    (14, '10.27.52.112', 'SIP Speaker Horn', '2n', 'beta', '10.27.58.82'),
    (15, '10.27.52.113', 'SIP Speaker', '2n', 'beta', '10.27.58.82')
     ]
