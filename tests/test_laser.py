import matplotlib.pyplot as plt
from movespad import laser

def test_hist_data():

    times = [1, 6, 11,12,13, 31, 35,38,44 ]
    clock= 5
    multi = 2

    res = laser.get_hist_data(times, clock, multi)

    assert res == [1, 1, 1, 2, 1, 0, 3, 4]


def test_centroid():

    data = [1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 4,4,4,4,4,4,4, 5,5]
    bins = [.5, 1.5, 2.5, 3.5, 4.5, 5.5, 6.5, 7.5, 8.5, 9.5, 10.5]
    counts = [2, 3, 6, 7, 2, 0, 0, 0, 0, 0]

    centroids, bfl = laser.get_centroids(bins, counts, data, real_value=0)

    assert centroids['max']==4
    assert centroids['mean']==3.2
    assert centroids['10perc']==4