from ir_client.cars.mappers import map_cars
from ir_client.series_race_results.mappers import map_series_race_results
from ir_client.subsession_results.mappers import map_subsession_results
from ir_client.laps.mappers import map_laps
from ir_client.utils.url_utils import build_relative_url, UrlWrapper
from abc import ABCMeta, abstractmethod

MEMBERSITE_PATH = build_relative_url("membersite", "member")
MEMBERSTATS_PATH = build_relative_url("memberstats", "member")


class Endpoint:
    def __init__(self, path, resource):
        self.path = path
        self.resource = resource


class EndpointType(metaclass=ABCMeta):
    def __init__(self, endpoint, mapper):
        self.endpoint = endpoint
        self.mapper = mapper

    def url(self, base_url: UrlWrapper):
        return base_url.resolve(self.endpoint.path).resolve(self.endpoint.resource)

    def map_data(self, data):
        return self.mapper(self.extract_data(data))
    
    @abstractmethod
    def extract_data(self, data):
        pass


class JsonEndpointType(EndpointType, metaclass=ABCMeta):
    def extract_data(self, data):
        return data.json()


class HtmlEndpointType(EndpointType, metaclass=ABCMeta):
    def extract_data(self, data):
        return data.text


class GetCars(HtmlEndpointType):
    def __init__(self):
        # TODO improve 2nd parameter
        endpoint = Endpoint(MEMBERSITE_PATH, build_relative_url(leaf="Home.do"))
        mapper = map_cars
        super().__init__(endpoint, mapper)


class GetSubsessionResults(JsonEndpointType):
    def __init__(self):
        # TODO improve 2nd parameter
        endpoint = Endpoint(MEMBERSITE_PATH, build_relative_url(leaf="GetSubsessionResults"))
        mapper = map_subsession_results
        super().__init__(endpoint, mapper)


class GetLaps(JsonEndpointType):
    def __init__(self):
        # TODO improve 2nd parameter
        endpoint = Endpoint(MEMBERSITE_PATH, build_relative_url(leaf="GetLaps"))
        mapper = map_laps
        super().__init__(endpoint, mapper)


class GetSeriesRaceResults(JsonEndpointType):
    def __init__(self):
        # TODO improve 2nd parameter
        endpoint = Endpoint(MEMBERSTATS_PATH, build_relative_url(leaf="GetSeriesRaceResults"))
        mapper = map_series_race_results
        super().__init__(endpoint, mapper)
