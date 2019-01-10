workflow "Find flag references" {
  on = "push"
  resolves = ["find_flags"]
}

action "find_flags" {
  secrets = [
    "LD_ACCESS_TOKEN",
  ]
  env = {
    LD_EXCLUDE = "app/static/.*"
    LD_PROJ_KEY = "support-service"
    LD_CONTEXT_LINES = "3"
  }
  uses = "docker://ldactions/git-flag-parser-gh-action:latest"
}
