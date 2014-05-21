# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

# More Data Mining with Weka - Class 3.5
# Copyright (C) 2014 Fracpete (fracpete at gmail dot com)

# TODO
# wherever your datasets are located
data_dir = "/some/where/data"

import os
import weka.core.jvm as jvm
import weka.core.packages as packages
from weka.core.converters import Loader
from weka.clusterers import Clusterer, ClusterEvaluation
from weka.filters import Filter
import weka.plot.graph as plg

jvm.start(packages=True)

pkg = "XMeans"
if not packages.is_installed(pkg):
    if not packages.install_package(pkg):
        raise Exception("Failed to install " + pkg)
    else:
        print("Installed " + pkg + ", please restart!")

# load weather.numeric
fname = data_dir + os.sep + "weather.numeric.arff"
print("\nLoading dataset: " + fname + "\n")
loader = Loader(classname="weka.core.converters.ArffLoader")
data = loader.load_file(fname)

# build KMeans
seeds = [-1, 11, 12]
for seed in seeds:
    if seed == -1:
        seedStr = "default"
    else:
        seedStr = str(seed)
    print("\n--> SimpleKMeans - seed " + seedStr + "\n")
    cl = Clusterer("weka.clusterers.SimpleKMeans")
    if seed != -1:
        cl.set_options(["-S", str(seed)])
    cl.build_clusterer(data)
    evl = ClusterEvaluation()
    evl.set_model(cl)
    evl.test_model(data)
    print(evl.get_cluster_results())

# build XMeans
print("\n--> XMeans\n")
flt = Filter(classname="weka.filters.unsupervised.attribute.RemoveType", options=["-T", "numeric", "-V"])
flt.set_inputformat(data)
filtered = flt.filter(data)
cl = Clusterer(classname="weka.clusterers.XMeans")
cl.build_clusterer(filtered)
evl = ClusterEvaluation()
evl.set_model(cl)
evl.test_model(filtered)
print(evl.get_cluster_results())

# build EM
print("\n--> EM\n")
cl = Clusterer(classname="weka.clusterers.EM", options=["-N", "2"])
cl.build_clusterer(data)
evl = ClusterEvaluation()
evl.set_model(cl)
evl.test_model(data)
print(evl.get_cluster_results())

# build Cobweb
print("\n--> Cobweb\n")
cl = Clusterer(classname="weka.clusterers.Cobweb", options=["-C", "0.3"])
cl.build_clusterer(data)
evl = ClusterEvaluation()
evl.set_model(cl)
evl.test_model(data)
print(evl.get_cluster_results())
plg.plot_dot_graph(cl.graph())

jvm.stop()