# -*- coding: utf-8 -*-

from openfisca_country_template.situation_examples import single

from openfisca_core.simulations import Simulation

from .test_countries import tax_benefit_system

scenario = tax_benefit_system.new_scenario().init_from_attributes(
    period=2014
    )


def test_calculate_with_trace():
    simulation = scenario.new_simulation(trace=True)
    simulation.calculate('disposable_income', "2014-01")


def test_clone():
    simulation = Simulation(
        tax_benefit_system = tax_benefit_system,
        simulation_json = {
            "persons": {
                "bill": {"salary": {"2017-01": 3000}},
                },
            "households": {
                "household": {
                    "parents": ["bill"]
                    }
                }
            })

    simulation_clone = simulation.clone()
    assert simulation != simulation_clone

    for entity_id, entity in simulation.entities.items():
        assert entity != simulation_clone.entities[entity_id]
        assert entity.entities_json == simulation_clone.entities[entity_id].entities_json

    assert simulation.persons != simulation_clone.persons

    salary_holder = simulation.person.get_holder('salary')
    salary_holder_clone = simulation_clone.person.get_holder('salary')

    assert salary_holder != salary_holder_clone
    assert salary_holder_clone.simulation == simulation_clone
    assert salary_holder_clone.entity == simulation_clone.person


def test_get_memory_usage():
    simulation = Simulation(tax_benefit_system = tax_benefit_system, simulation_json = single)
    simulation.calculate('disposable_income', '2017-01')
    memory_usage = simulation.get_memory_usage(variables = ['salary'])
    assert(memory_usage['total_nb_bytes'] > 0)
    assert(len(memory_usage['by_variable']) == 1)
