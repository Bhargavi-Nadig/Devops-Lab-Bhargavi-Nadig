
import docker

# Connect to Docker
client = docker.from_env()

# Build the Docker image
client.images.build(path=".", tag="flask-apparmor")

print("Image built successfully.")

# Try to run the container with the AppArmor profile
try:
    container = client.containers.run(
        "flask-apparmor",
        name="flask-apparmor-test",
        ports={"5000/tcp": 5000},
        security_opt=["apparmor=my-apparmor-profile"],
        detach=True,
        remove=True
    )

    print(f"Container started: {container.short_id}")

    # Inspect the container's configured security options
    info = client.api.inspect_container(container.id)
    print("Security options:", info["HostConfig"]["SecurityOpt"])
    print("AppArmor profile:", info.get("AppArmorProfile"))

    container.stop()

except docker.errors.APIError as error:
    print("Docker could not start the container with this profile.")
    print(error)

finally:
    # Remove the earlier Flask container if it is still running
    try:
        old_container = client.containers.get("flask-secure")
        old_container.stop()
        old_container.remove()
        print("Removed the earlier flask-secure container.")
    except docker.errors.NotFound:
        pass
