class TestHelpers:
    def assert_equal_elements(self, list_one, list_two):
        self.assert_is_same_length(list_one, list_two)
        for el in list_one:
            assert el in list_two

    def assert_is_same_length(self, list_one, list_two):
        assert len(list_one) == len(list_two)
