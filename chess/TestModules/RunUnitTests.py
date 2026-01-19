from TestModules.RookTests import RookTests

def run_unit_tests():
    rook_test_obj = RookTests()

    rook_test_obj.run_all()
    print("finished with unit tests")

print("starting")
run_unit_tests()
