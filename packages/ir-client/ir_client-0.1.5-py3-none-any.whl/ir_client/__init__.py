"""
ir-client library
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

ir-client is a library to retrieve data from the iRacing API.

Pull subsession results:
    >>> import ir_client
    >>> endpoint_parameters = ir_client.GetSubsessionResultsParameters(123456)
    >>> session_parameters = ir_client.SessionParameters('some_cookie')
    >>> client = ir_client.IracingClient()
    >>> client.get_data(
    ...     ir_client.GetSubsessionResults,
    ...     endpoint_parameters,
    ...     session_parameters)
"""

from .iracing_client import IracingClient

from .session_parameters import SessionParameters

from .endpoint_parameters import EmptyParameters
from .endpoint_parameters import GetSubsessionResultsParameters
from .endpoint_parameters import GetLapsParameters
from .endpoint_parameters import GetSeriesRaceResultsParameters

from .endpoint_types import GetCars
from .endpoint_types import GetSubsessionResults
from .endpoint_types import GetLaps
from .endpoint_types import GetSeriesRaceResults

from .cars.models import Car, Cars
from .subsession_results.models import SimSession, SimSessionType
from .laps.models import LapEvent, Lap
from .series_race_results.models import SeriesRaceResult
