import socket

running_in_docker = socket.gethostname().startswith("docker-usf-")


def host_for_dependency(
    addres_for_docker: str, address_for_localhost: str = "127.0.0.1"
) -> str:
    if running_in_docker:
        return addres_for_docker
    else:
        return address_for_localhost

