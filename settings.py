import os
import statsd
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="DYNACONF",
    settings_files=['./config.yaml'],
)


base_path = os.path.dirname(os.path.abspath(__file__))
statsd = statsd.StatsClient(host=settings.statsd.statsd_host, port=settings.statsd.statsd_port)