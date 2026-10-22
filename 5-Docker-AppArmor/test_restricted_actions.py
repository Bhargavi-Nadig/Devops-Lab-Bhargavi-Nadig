
import docker

client = docker.from_env()

container = client.containers.run(
    "flask-apparmor",
    name="flask-restriction-test",
    security_opt=["apparmor=my-apparmor-profile"],
    detach=True
)

print(f"Container started: {container.short_id}")

try:
    # Test 1: Read a restricted file
    exit_code, output = container.exec_run(
        ["python", "-c",
         "open('/etc/passwd').read(); print('File read succeeded')"]
    )
    print("\nTest 1: Read /etc/passwd")
    print("Exit code:", exit_code)
    print("Output:", output.decode().strip())

    # Test 2: Execute a shell
    exit_code, output = container.exec_run(
        ["/bin/bash", "-c", "echo Shell executed"]
    )
    print("\nTest 2: Execute /bin/bash")
    print("Exit code:", exit_code)
    print("Output:", output.decode().strip())

finally:
    container.stop()
    container.remove()
    print("\nContainer stopped and removed.")
