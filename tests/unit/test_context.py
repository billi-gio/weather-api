from weather_api.context import (
    DependencyContext,
    OverriddenComponents,
    get_dependency_context,
    get_overridden_components,
)


class TestDependencyContext:
    def test_overrides_config(self, application_config):
        # given
        config = application_config.copy()
        overridden_components = OverriddenComponents(app_config=config)

        # when
        context = DependencyContext(
            app_config=application_config, overridden_components=overridden_components
        )

        # then
        assert context.config is overridden_components.config

    def test_returns_same_instance_of_overridden_components(self):
        # when
        components_one = get_overridden_components()
        components_two = get_overridden_components()

        # then
        assert components_one is components_two

    def test_returns_same_instance_of_dependency_context(self):
        # when
        context_one = get_dependency_context(get_overridden_components())
        context_two = get_dependency_context(get_overridden_components())

        # then
        assert context_one is context_two
