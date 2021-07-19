"Conditinal mock Roxar API for unit tests."
from enum import Enum, unique

class MockSurveyPointSeries:
    "Mock Roxar API SurveyPointSeries."
    @classmethod
    def get_measured_depths_and_points(cls):
        try:
            import numpy as np
            return np.array([[1,2], [3,4], [5,6]])

        except ModuleNotFoundError:
            return None

    @classmethod
    def interpolate_survey_point(cls, md):
        try:
            import numpy as np
            return np.array([md])

        except ModuleNotFoundError:
            return None

class MockWellBoreReference:
    name = None

class MockTrajectoryReference:
    wellbore = MockWellBoreReference
    survey_point_series = MockSurveyPointSeries()

@unique
class MockLogCurveInterpolationType(Enum):
    "Mock Roxar API Log curve interpolation type enum"
    continuous = 1
    interval = 2
    point = 3

class MockLogCurve:
    "Mock Roxar API Log Curve."
    name = "DiscreteLog"
    kind = "integer"
    unit = "m"
    is_discrete = True
    interpolation_type = MockLogCurveInterpolationType.interval
    shape = (2,1)

    @classmethod
    def get_code_names(cls):
        return {1: "One"}

    @classmethod
    def get_values(cls):
        try:
            import numpy as np
            return np.array([1,2])

        except ModuleNotFoundError:
            return None

class MockLogRun:
    "Mock Roxar API Log Run."
    name = "LogRun"
    log_curves = [MockLogCurve()]
    trajectory = MockTrajectoryReference

    @classmethod
    def get_measured_depths(cls):
        return [1,100]

class MockTrajectory:
    "Mock Roxar API Trajectories."
    log_runs = [MockLogRun()]
    survey_point_series = MockSurveyPointSeries()

class MockWellBore:
    "Mock Roxar API WellBore."
    name = None
    trajectories = [MockTrajectory()]

class MockWell:
    "Mock Roxar API Well."
    name = None
    wellhead = None
    wellbore = MockWellBore()

class MockFeature:
    "Mock Roxar API geological feature."
    def __init__(self, name):
        self.name = name

class MockZone(MockFeature):
    "Mock Roxar API Zone."
    def __init__(self, name, horizon_above, horizon_below):
        MockFeature.__init__(self, name)
        self.horizon_above = horizon_above
        self.horizon_below = horizon_below

class MockHorizonContainer(list):
    "Mock Roxar API horizon container."

    def create(self, name, horizon_type):
        "Create mock horizon."
        assert horizon_type is not None
        horizon = MockFeature(name)
        self.append(horizon)
        return horizon

class MockZoneContainer(list):
    "Mock Roxar API zone container."
    def create(self, name, horizon_above, horizon_below):
        "Create mock zone."
        zone = MockZone(name, horizon_above, horizon_below)
        self.append(zone)
        return zone

class MockProject:
    "Mock Roxar API project."
    zones = MockZoneContainer()
    horizons = MockHorizonContainer()

    def open(self, *args, **kwargs):
        "Not implemented."
        raise NotImplementedError("Not supported.")

class MockHorizonType:
    "Mock Roxar API HorizonType."
    calculated = True

def conditional_well_type():
    "Conditionally get well type."

    try:
        import roxar
        import roxar.wells

        class RoxarWell(roxar.wells.Well):
            "Roxar API well wrapper."
            name = None
            wellhead = None
            wellbore = MockWellBore()
            def __init__(self):
                pass

        return RoxarWell

    except ModuleNotFoundError:
        return MockWell

def conditional_project_type():
    "Conditionally get project type."
    try:
        import roxar
        import roxar._testing

        class RoxarProject(roxar.Project):
            "Roxar API project wrapper."
            def __new__(cls):
                project = roxar._testing.create_example(
                    roxar._testing.Example.none)
                return project

        return RoxarProject

    except ModuleNotFoundError:
        return MockProject

def conditional_horizon_type_type():
    "Conditionally get HorizonType type."

    try:
        import roxar
        return roxar.HorizonType
    except ModuleNotFoundError:
        return MockHorizonType


Well = conditional_well_type()

Project = conditional_project_type()

HorizonType = conditional_horizon_type_type()
