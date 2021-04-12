class MockWellBore:
    trajectories = ()

class MockWell:
    name = None
    wellhead = None
    wellbore = MockWellBore()

class MockFeature:
    def __init__(self, name):
        self.name = name

class MockZone(MockFeature):
    def __init__(self, name, horizon_above, horizon_below):
        MockFeature.__init__(self, name)
        self.horizon_above = horizon_above
        self.horizon_below = horizon_below

class MockHorizonContainer(list):
    def create(self, name, horizon_type):
        horizon = MockFeature(name)
        self.append(horizon)
        return horizon

class MockZoneContainer(list):
    def create(self, name, horizon_above, horizon_below):
        zone = MockZone(name, horizon_above, horizon_below)
        self.append(zone)
        return zone

class MockProject:
    zones = MockZoneContainer()
    horizons = MockHorizonContainer()

    def open(*args, **kwargs):
        raise NotImplementedError("Not supported.")

class MockHorizonType:
    calculated = None

def conditional_well_type():
    try:
        import roxar
        import roxar.wells

        class Well(roxar.wells.Well):
            name = None
            wellhead = None
            wellbore = MockWellBore()
            def __init__(self):
                pass

        return Well

    except ModuleNotFoundError:
        return MockWell

def conditional_project_type():
    try:
        import roxar
        import roxar._testing

        class Project(roxar.Project):
            def __new__(cls):
                project = roxar._testing.create_example(
                        roxar._testing.Example.none)
                return project

        return Project

    except ModuleNotFoundError:
        return MockProject

def conditional_horizon_type_type():
    try:
        import roxar
        return roxar.HorizonType
    except ModuleNotFoundError:
        return MockHorizonType


Well = conditional_well_type()

Project = conditional_project_type()

HorizonType = conditional_horizon_type_type()
