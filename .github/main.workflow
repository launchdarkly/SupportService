workflow "Find flag references" {
  on = "push"
  resolves = ["find_flags"]
}

action "find_flags" {
  secrets = [
    "LD_ACCESS_TOKEN",
  ]
  env = {
    LD_PROJ_KEY = "default"
  }
  uses = "docker://ldactions/git-flag-parser-gh-action:latest"
}
