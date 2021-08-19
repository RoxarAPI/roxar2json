"Conditinal mock Roxar API for unit tests."
from enum import Enum, unique
import numpy as np

ROXAR_FOUND = True

try:
    import roxar
    import roxar.wells
    import roxar._testing
except ModuleNotFoundError:
    ROXAR_FOUND = False

PROJECT = None


class ProjectSingleton:
    project = None


class MockSurveyPointSeries:
    "Mock Roxar API SurveyPointSeries."

    def __init__(self):
        self.survey_points = None

    def get_measured_depths_and_points(self):
        return self.survey_points

    def set_measured_depths_and_points(self, value):
        self.survey_points = np.array(value)

    @classmethod
    def interpolate_survey_point(cls, md):
        return np.array([md])


class MockWellBoreReference:
    name = "Well"


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
    kind = "discrete"
    unit = "DISC"
    is_discrete = True
    interpolation_type = MockLogCurveInterpolationType.interval
    shape = (2, 1)

    def get_code_names(self):
        return self.code_names

    def __init__(self):
        self.values = None
        self.code_names = None

    def get_values(self):
        return self.values

    def set_values(self, values):
        self.values = np.array(values)

    def set_code_names(self, name_map):
        self.code_names = name_map


class MockLogCurves(list):
    "Mock Roxar API log curve container."

    def create_discrete(self, _):
        curve = MockLogCurve()
        self.append(curve)
        return curve


class MockLogRun:
    "Mock Roxar API Log Run."

    name = "LogRun"
    trajectory = MockTrajectoryReference

    def __init__(self):
        self.log_curves = MockLogCurves()
        self.measured_depths = np.array([])

    def set_measured_depths(self, value):
        self.measured_depths = np.array(value)

    def get_measured_depths(self):
        return self.measured_depths


class MockLogRunContainer(list):
    "Mock Roxar API log run container."

    def create(self, _):
        "Create mock log run."
        log_run = MockLogRun()
        self.append(log_run)
        return log_run


class MockTrajectory:
    "Mock Roxar API Trajectories."
    log_runs = MockLogRunContainer()
    survey_point_series = MockSurveyPointSeries()


class MockTrajectoryContainer(list):
    "Mock Roxar API trajectory container."

    def create(self, _):
        "Create mock trajectory."
        trajectory = MockTrajectory()
        self.append(trajectory)
        return trajectory


class MockWellBore:
    "Mock Roxar API WellBore."
    name = "Well"
    trajectories = MockTrajectoryContainer()


class MockWell:
    "Mock Roxar API Well."
    name = "Well"
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


class MockWellContainer(list):
    "Mock Roxar API well container."

    def create(self, _):
        "Create mock well."
        well = MockWell()
        self.append(well)
        return well


class MockProject:
    "Mock Roxar API project."
    zones = MockZoneContainer()
    horizons = MockHorizonContainer()
    wells = MockWellContainer()

    def open(self, *args, **kwargs):
        "Not implemented."
        raise NotImplementedError("Not supported.")


class MockHorizonType:
    "Mock Roxar API HorizonType."
    calculated = True


def conditional_well_type():
    "Conditionally get well type."

    if not ROXAR_FOUND:
        return MockWell

    class RoxarWell(roxar.wells.Well):
        "Roxar API well wrapper."
        name = None
        wellhead = None
        wellbore = MockWellBore()

        def __init__(self):
            pass

    return RoxarWell


def conditional_project_type():
    "Conditionally get project type."
    if not ROXAR_FOUND:
        return MockProject

    class RoxarProject(roxar.Project):
        "Roxar API project wrapper."

        def __new__(cls):
            if not ProjectSingleton.project:
                ProjectSingleton.project = roxar._testing.create_example(
                    roxar._testing.Example.none
                )
            return ProjectSingleton.project

    return RoxarProject


def conditional_horizon_type_type():
    "Conditionally get HorizonType type."

    if not ROXAR_FOUND:
        return MockHorizonType

    return roxar.HorizonType


def conditional_trajectory_type():
    "Conditionally get trajectory type."

    if not ROXAR_FOUND:
        return MockTrajectory

    class RoxarTrajectory(roxar.wells.Trajectory):
        "Roxar Trajectory wrapper."

        def __new__(cls):
            ProjectType = conditional_project_type()
            project = ProjectType()
            wells = project.wells
            well = wells.create("Well")
            wellbore = well.wellbore
            trajectory = wellbore.trajectories.create("_")
            return trajectory

    return RoxarTrajectory


def conditional_log_run_type():
    "Conditionally get log run type."

    if not ROXAR_FOUND:
        return MockLogRun

    class RoxarLogRun(roxar.wells.LogRun):
        "Roxar LogRun wrapper."

        def __new__(cls):
            TrajectoryType = conditional_trajectory_type()
            trajectory = TrajectoryType()
            log_runs = trajectory.log_runs
            log_run = log_runs.create("LogRun")
            return log_run

    return RoxarLogRun


def conditional_log_curve_interpolation_type_type():
    "Conditionally get log curve interpolation type"
    if not ROXAR_FOUND:
        return MockLogCurveInterpolationType
    return roxar.LogCurveInterpolationType


Well = conditional_well_type()

Project = conditional_project_type()

HorizonType = conditional_horizon_type_type()

Trajectory = conditional_trajectory_type()

LogRun = conditional_log_run_type()

LogCurveInterpolationType = conditional_log_curve_interpolation_type_type()
