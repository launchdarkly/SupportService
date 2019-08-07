workflow "Find code references" {
  on = "push"
  resolves = ["launchdarkly/find-code-references"]
}

action "launchdarkly/find-code-references" {
  uses = "launchdarkly/find-code-references"
  secrets = ["LD_ACCESS_TOKEN", "GITHUB_TOKEN"]
  env = {
    LD_EXCLUDE = "app/static/.*"
  }
}
