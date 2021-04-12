class MockWellBore:
    trajectories = ()

class MockWell:
    name = None
    wellhead = None
    wellbore = MockWellBore()

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

def create_example_well():
    try:
        import roxar
        import roxar._testing
        project = roxar._testing.create_example(Example.wells)
        return project.wells[0]
    except ModuleNotFoundError:
        return MockWell


Well = conditional_well_type()

