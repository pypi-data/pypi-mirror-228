import pytest


@pytest.mark.parametrize("zi,correct_P", [
    (True, [
        [2./3.,0.,1./3.],
        [1./3.,2./3.,0.],
        [0., 1./3., 2./3.]
    ]),
    (False,[
        [ 1./2., 0, 1./2.],
        [ 1./2., 1./2., 0],
        [ 0,  1./2., 1./2.]
    ])
])
def test_condorcet(zi, correct_P):
    import gridvoting as gv
    xp = gv.xp
    condorcet_model =  gv.CondorcetCycle(zi=zi)
    assert not condorcet_model.analyzed
    condorcet_model.analyze()
    assert condorcet_model.analyzed
    mc = condorcet_model.MarkovChain
    gv.xp.testing.assert_array_almost_equal(
        mc.P,
        xp.array(correct_P),
        decimal=10
    )
    gv.xp.testing.assert_array_almost_equal(
        condorcet_model.stationary_distribution,
        xp.array([1.0/3.0,1.0/3.0,1.0/3.0]),
        decimal=10
    )
    mc=condorcet_model.MarkovChain
    alt = mc.solve_for_unit_eigenvector()
    gv.xp.testing.assert_array_almost_equal(
        alt,
        xp.array([1.0/3.0,1.0/3.0,1.0/3.0]),
        decimal=10
    )

