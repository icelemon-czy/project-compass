#!/usr/bin/env ruby
# frozen_string_literal: true

require "json"
require "pathname"
require "yaml"

ROOT = Pathname.new(__dir__).join("..").expand_path
TEMPLATE_ROOT = ROOT.join("templates/compass-harness")
MANIFEST_PATH = TEMPLATE_ROOT.join("manifest.yaml")
SKILLS_ROOT = ROOT.join(".agents/skills")
LEGACY_AI_REFERENCE = /(?<![A-Za-z0-9-])\.ai(?:\/|\b)/

errors = []

def add_error(errors, message)
  errors << message
end

def load_yaml(path, errors)
  YAML.safe_load(path.read, permitted_classes: [], permitted_symbols: [], aliases: false)
rescue StandardError => e
  add_error(errors, "#{path.relative_path_from(ROOT)}: invalid YAML (#{e.message})")
  nil
end

required_templates = %w[
  manifest.yaml
  installed-manifest.yaml.template
  config.yaml
  agent-rules/AGENTS.global.md
  agent-rules/AGENTS.project.md
  context/README.md
  skills/_skill-template/SKILL.md
  subagents/_subagent-template.md
  subagents/examples/codebase-explorer.md
  subagents/examples/impact-analyst.md
  subagents/examples/test-reviewer.md
  subagents/examples/spec-validator.md
  adapters/codex/AGENTS.md.template
  adapters/codex/config.toml.template
  adapters/codex/agent.toml.template
  adapters/claude-code/CLAUDE.md.template
  adapters/claude-code/agent.md.template
  adapters/opencode/AGENTS.md.template
  adapters/opencode/opencode.json.template
  adapters/opencode/agent.md.template
]

required_templates.each do |relative|
  path = TEMPLATE_ROOT.join(relative)
  add_error(errors, "missing template: #{path.relative_path_from(ROOT)}") unless path.file?
end

manifest = MANIFEST_PATH.file? ? load_yaml(MANIFEST_PATH, errors) : nil
if manifest
  add_error(errors, "manifest schema_version must be 1") unless manifest["schema_version"] == 1
  expected_platforms = %w[codex claude-code opencode]
  unless manifest["supported_platforms"] == expected_platforms
    add_error(errors, "manifest supported_platforms must be exactly: #{expected_platforms.join(', ')}")
  end

  conventions = manifest["conventions"] || {}
  required_conventions = %w[
    placeholder_format
    required_placeholder_missing
    optional_placeholder_missing
    relative_references
    skill_directory
    skill_frontmatter_fields
    adapter_template_suffix
  ]
  missing_conventions = required_conventions - conventions.keys
  add_error(errors, "manifest missing conventions: #{missing_conventions.join(', ')}") unless missing_conventions.empty?

  installation = manifest["installation"] || {}
  add_error(errors, "manifest canonical_root must be .compass-harness") unless installation["canonical_root"] == ".compass-harness"

  expected_canonical_targets = {
    "manifest" => ".compass-harness/manifest.yaml",
    "config" => ".compass-harness/config.yaml",
    "global_rules" => ".compass-harness/rules/global.md",
    "project_rules" => ".compass-harness/rules/project.md",
    "context" => ".compass-harness/context",
    "skills" => ".compass-harness/skills",
    "subagents" => ".compass-harness/subagents"
  }
  unless installation["canonical_targets"] == expected_canonical_targets
    add_error(errors, "manifest canonical_targets must define the complete .compass-harness installation tree")
  end

  expected_generated_adapters = {
    "codex" => { "project_rules" => "AGENTS.md", "skills" => ".agents/skills", "subagents" => ".codex/agents" },
    "claude-code" => { "project_rules" => "CLAUDE.md", "skills" => ".claude/skills", "subagents" => ".claude/agents" },
    "opencode" => { "project_rules" => "AGENTS.md", "config" => "opencode.json", "skills" => ".agents/skills", "subagents" => ".opencode/agents" }
  }
  unless installation["generated_adapters"] == expected_generated_adapters
    add_error(errors, "manifest generated_adapters do not match the three supported platforms")
  end

  expected_policy = {
    "canonical_content_is_editable" => true,
    "generated_adapters_are_editable" => false,
    "generated_adapters_must_be_rebuildable" => true
  }
  add_error(errors, "manifest installation policy must make adapters non-editable and rebuildable") unless installation["policy"] == expected_policy

  (manifest["sources"] || {}).each do |name, relative|
    path = TEMPLATE_ROOT.join(relative).cleanpath
    add_error(errors, "manifest source #{name} does not exist: #{relative}") unless path.exist?
  end
end

skill_files = SKILLS_ROOT.glob("*/SKILL.md").sort
add_error(errors, "expected 13 skills under .agents/skills, found #{skill_files.length}") unless skill_files.length == 13

skill_files.each do |path|
  content = path.read
  match = content.match(/\A---\n(.*?)\n---\n/m)
  unless match
    add_error(errors, "#{path.relative_path_from(ROOT)}: missing top YAML frontmatter")
    next
  end

  metadata = YAML.safe_load(match[1], permitted_classes: [], permitted_symbols: [], aliases: false)
  unless metadata.is_a?(Hash) && metadata.keys.sort == %w[description name]
    add_error(errors, "#{path.relative_path_from(ROOT)}: frontmatter must contain only name and description")
    next
  end

  name = metadata["name"]
  folder = path.dirname.basename.to_s
  add_error(errors, "#{path.relative_path_from(ROOT)}: name '#{name}' must match folder '#{folder}'") unless name == folder
  add_error(errors, "#{path.relative_path_from(ROOT)}: invalid skill name '#{name}'") unless name.match?(/\A[a-z0-9-]{1,64}\z/)
  add_error(errors, "#{path.relative_path_from(ROOT)}: description must be non-empty") if metadata["description"].to_s.strip.empty?

  obsolete_references = content.scan(%r{(?:builders/(?:copilot|cline)|entrypoints/(?:copilot-instructions|clinerules)|\.github/skills)}i).uniq
  unless obsolete_references.empty?
    add_error(errors, "#{path.relative_path_from(ROOT)}: obsolete platform references: #{obsolete_references.join(', ')}")
  end
  add_error(errors, "#{path.relative_path_from(ROOT)}: legacy .ai path must use .compass-harness/context") if content.match?(LEGACY_AI_REFERENCE)
end

installed_manifest_path = TEMPLATE_ROOT.join("installed-manifest.yaml.template")
if installed_manifest_path.file?
  installed_manifest = load_yaml(installed_manifest_path, errors)
  if installed_manifest
    add_error(errors, "installed manifest canonical_root must be .compass-harness") unless installed_manifest["canonical_root"] == ".compass-harness"
    canonical_paths = installed_manifest["canonical_paths"] || {}
    unless canonical_paths.values.all? { |path| path.start_with?(".compass-harness/") }
      add_error(errors, "installed manifest canonical paths must stay under .compass-harness/")
    end
  end
end

config_path = TEMPLATE_ROOT.join("config.yaml")
if config_path.file?
  config = load_yaml(config_path, errors)
  if config
    add_error(errors, "config schema_version must be 1") unless config["schema_version"] == 1
    add_error(errors, "config platforms must match supported platforms") unless config["platforms"] == %w[codex claude-code opencode]
    add_error(errors, "config canonical_root must be .compass-harness") unless config.dig("generation", "canonical_root") == ".compass-harness"
  end
end

skill_template = TEMPLATE_ROOT.join("skills/_skill-template/SKILL.md")
if skill_template.file?
  match = skill_template.read.match(/\A---\n(.*?)\n---\n/m)
  if match
    metadata = YAML.safe_load(match[1], permitted_classes: [], permitted_symbols: [], aliases: false)
    unless metadata.is_a?(Hash) && metadata.keys.sort == %w[description name]
      add_error(errors, "#{skill_template.relative_path_from(ROOT)}: frontmatter must contain only name and description")
    end
  else
    add_error(errors, "#{skill_template.relative_path_from(ROOT)}: missing top YAML frontmatter")
  end
end

subagent_contracts = {
  "subagents/_subagent-template.md" => %w[Purpose Access Instructions Forbidden Output],
  "subagents/examples/codebase-explorer.md" => %w[Purpose Access Instructions Output],
  "subagents/examples/impact-analyst.md" => %w[Purpose Access Instructions Output],
  "subagents/examples/test-reviewer.md" => %w[Purpose Access Instructions Output],
  "subagents/examples/spec-validator.md" => %w[Purpose Access Instructions Output]
}
subagent_contracts.each do |relative, headings|
  path = TEMPLATE_ROOT.join(relative)
  next unless path.file?

  headings.each do |heading|
    add_error(errors, "#{path.relative_path_from(ROOT)}: missing #{heading} section") unless path.read.match?(/^## #{Regexp.escape(heading)}\b/)
  end
end

%w[adapters/claude-code/agent.md.template adapters/opencode/agent.md.template].each do |relative|
  path = TEMPLATE_ROOT.join(relative)
  next unless path.file?

  match = path.read.match(/\A---\n(.*?)\n---\n/m)
  unless match
    add_error(errors, "#{path.relative_path_from(ROOT)}: missing top YAML frontmatter")
    next
  end

  begin
    metadata = YAML.safe_load(match[1], permitted_classes: [], permitted_symbols: [], aliases: false)
    add_error(errors, "#{path.relative_path_from(ROOT)}: frontmatter must be a map") unless metadata.is_a?(Hash)
  rescue StandardError => e
    add_error(errors, "#{path.relative_path_from(ROOT)}: invalid YAML frontmatter (#{e.message})")
  end
end

registered_placeholders = []
if manifest
  registered_placeholders.concat((manifest["placeholders"] || {}).keys)
  registered_placeholders.concat(manifest["template_placeholders"] || [])
end

template_files = TEMPLATE_ROOT.glob("**/*").select(&:file?)
used_placeholders = template_files.flat_map { |path| path.read.scan(/\{\{([A-Z0-9_]+)\}\}/).flatten }.uniq.sort
unknown_placeholders = used_placeholders - registered_placeholders
unused_placeholders = registered_placeholders - used_placeholders
add_error(errors, "unregistered placeholders: #{unknown_placeholders.join(', ')}") unless unknown_placeholders.empty?
add_error(errors, "registered but unused placeholders: #{unused_placeholders.join(', ')}") unless unused_placeholders.empty?

legacy_path_files = template_files + ROOT.join("builders/claude").glob("**/*.md")
legacy_path_files.each do |path|
  add_error(errors, "#{path.relative_path_from(ROOT)}: legacy .ai path must use .compass-harness/context") if path.read.match?(LEGACY_AI_REFERENCE)
end

%w[
  adapters/codex/AGENTS.md.template
  adapters/claude-code/CLAUDE.md.template
  adapters/opencode/AGENTS.md.template
].each do |relative|
  path = TEMPLATE_ROOT.join(relative)
  next unless path.file?

  add_error(errors, "#{path.relative_path_from(ROOT)}: adapter must point to .compass-harness/") unless path.read.include?(".compass-harness/")
end

TEMPLATE_ROOT.glob("**/*.md*").each do |path|
  path.read.scan(/\[[^\]]*\]\(([^)]+)\)/).flatten.each do |target|
    next if target.start_with?("http://", "https://", "#", "mailto:")
    next if target.include?("{{")

    resolved = path.dirname.join(target.split("#", 2).first).cleanpath
    add_error(errors, "#{path.relative_path_from(ROOT)}: broken relative link #{target}") unless resolved.exist?
  end
end

opencode_template = TEMPLATE_ROOT.join("adapters/opencode/opencode.json.template")
if opencode_template.file?
  begin
    JSON.parse(opencode_template.read)
  rescue JSON::ParserError => e
    add_error(errors, "#{opencode_template.relative_path_from(ROOT)}: invalid JSON (#{e.message})")
  end
end

forbidden_instances = [
  ROOT.join("AGENTS.md"),
  ROOT.join("CLAUDE.md"),
  ROOT.join("opencode.json")
]
forbidden_instances.each do |path|
  add_error(errors, "Phase 2 must not install instance file: #{path.relative_path_from(ROOT)}") if path.exist?
end

obsolete_paths = %w[
  .github/skills
  builders/copilot
  builders/cline
  entrypoints/copilot-instructions.md
  entrypoints/clinerules.md
]
obsolete_paths.each do |relative|
  path = ROOT.join(relative)
  next unless path.exist?
  next if path.directory? && path.children.empty?

  add_error(errors, "obsolete platform asset still exists: #{relative}")
end

{
  ROOT.join(".codex/agents") => "*.toml",
  ROOT.join(".claude/agents") => "*.md",
  ROOT.join(".opencode/agents") => "*.md"
}.each do |directory, pattern|
  next unless directory.exist?
  add_error(errors, "Phase 2 must not install agent instances under #{directory.relative_path_from(ROOT)}") unless directory.glob(pattern).empty?
end

if errors.empty?
  puts "Phase 2 static validation passed: 13 skills, #{required_templates.length} required templates, #{used_placeholders.length} placeholders."
  exit 0
end

warn "Phase 2 static validation failed (#{errors.length} error#{errors.length == 1 ? '' : 's'}):"
errors.each { |error| warn "- #{error}" }
exit 1
