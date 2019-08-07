workflow "Find flag references" {
  on = "push"
  resolves = ["find_flags"]
}
action "find_flags" {
  secrets = [
    "LD_ACCESS_TOKEN",
  ]
  env = {
    LD_PROJ_KEY = "support-service"
  }
  uses = "docker://launchdarkly/ld-find-code-refs-github-action:1.1.1"
}
