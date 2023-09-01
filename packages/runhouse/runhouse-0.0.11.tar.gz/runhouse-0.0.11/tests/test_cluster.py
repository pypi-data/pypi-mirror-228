import copy
import unittest

import pytest

import runhouse as rh
from runhouse.rns.hardware import OnDemandCluster

from .conftest import cpu_clusters, summer


def is_on_cluster(cluster):
    return cluster.on_this_cluster()


@pytest.mark.clustertest
def test_cluster_config(ondemand_cpu_cluster):
    config = ondemand_cpu_cluster.config_for_rns
    cluster2 = OnDemandCluster.from_config(config)
    assert cluster2.address == ondemand_cpu_cluster.address


@pytest.mark.clustertest
@pytest.mark.rnstest
def test_cluster_sharing(ondemand_cpu_cluster):
    ondemand_cpu_cluster.share(
        users=["donny@run.house", "josh@run.house"],
        access_type="write",
        notify_users=False,
    )
    assert True


@pytest.mark.clustertest
def test_read_shared_cluster(ondemand_cpu_cluster):
    res = ondemand_cpu_cluster.run_python(["import numpy", "print(numpy.__version__)"])
    assert res[0][1]


@pytest.mark.clustertest
@cpu_clusters
def test_install(cluster):
    cluster.install_packages(
        [
            "./",
            "torch==1.12.1",
            # 'conda:jupyterlab',
            # 'gh:pytorch/vision'
        ]
    )


@pytest.mark.clustertest
@cpu_clusters
def test_basic_run(cluster):
    # Create temp file where fn's will be stored
    test_cmd = "echo hi"
    res = cluster.run(commands=[test_cmd])
    assert "hi" in res[0][1]


@pytest.mark.clustertest
@cpu_clusters
def test_restart_server(cluster):
    cluster.up_if_not()
    codes = cluster.restart_server(resync_rh=False)
    assert codes


@pytest.mark.clustertest
@cpu_clusters
def test_on_same_cluster(cluster):
    hw_copy = copy.copy(cluster)

    func_hw = rh.function(is_on_cluster).to(cluster)
    assert func_hw(cluster)
    assert func_hw(hw_copy)


@pytest.mark.clustertest
def test_on_diff_cluster(ondemand_cpu_cluster, byo_cpu):
    func_hw = rh.function(is_on_cluster).to(ondemand_cpu_cluster)
    assert not func_hw(byo_cpu)


@pytest.mark.clustertest
def test_byo_cluster(byo_cpu, local_folder):
    assert byo_cpu.is_up()

    summer_func = rh.function(summer).to(byo_cpu)
    assert summer_func(1, 2) == 3

    byo_cpu.put("test_obj", list(range(10)))
    assert byo_cpu.get("test_obj") == list(range(10))

    local_folder = local_folder.to(byo_cpu)
    assert "sample_file_0.txt" in local_folder.ls(full_paths=False)


@pytest.mark.clustertest
def test_byo_proxy(byo_cpu, local_folder):
    rh.rh_config.open_cluster_tunnels.pop(byo_cpu.address)
    byo_cpu.client = None
    # byo_cpu._rpc_tunnel.close()
    byo_cpu._rpc_tunnel = None

    byo_cpu._ssh_creds["ssh_host"] = "127.0.0.1"
    byo_cpu._ssh_creds.update(
        {"ssh_proxy_command": "ssh -W %h:%p ubuntu@test-byo-cluster"}
    )
    assert byo_cpu.up_if_not()

    status, stdout, _ = byo_cpu.run(["echo hi"])[0]
    assert status == 0
    assert stdout == "hi\n"

    summer_func = rh.function(summer, env=rh.env(working_dir="local:./")).to(byo_cpu)
    assert summer_func(1, 2) == 3

    byo_cpu.put("test_obj", list(range(10)))
    assert byo_cpu.get("test_obj") == list(range(10))

    # TODO: uncomment out when in-mem lands
    # local_folder = local_folder.to(byo_cpu)
    # assert "sample_file_0.txt" in local_folder.ls(full_paths=False)


if __name__ == "__main__":
    unittest.main()
