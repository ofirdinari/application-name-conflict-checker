from application_conflict_checker import repo_has_name_collision
import consts

repo_path = consts.REPO_PATH
cluster = consts.CHOSEN_CLUSTER
token = consts.TOKEN

if repo_has_name_collision(repo_path, cluster, token):
    print("❌ Cannot deploy — name collision detected")
else:
    print("✅ Safe to deploy")
