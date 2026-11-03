// Regenerates the "Recent releases" block of profile/README.md from the public repositories' GitHub releases.
// Usage: node scripts/recent-releases.mjs [profile/README.md]   (needs an authenticated gh CLI)
import { execFileSync } from 'node:child_process'
import { readFileSync, writeFileSync } from 'node:fs'

const ORG = 'crewloom'
const LIMIT = 6
const file = process.argv[2] ?? 'profile/README.md'
const gh = (...args) => JSON.parse(execFileSync('gh', args, { encoding: 'utf8' }))

const repos = gh('repo', 'list', ORG, '--visibility', 'public', '--no-archived', '--json', 'name').map(r => r.name)
const releases = repos.flatMap(repo =>
  gh('release', 'list', '-R', `${ORG}/${repo}`, '--limit', String(LIMIT), '--exclude-drafts', '--exclude-pre-releases', '--json', 'name,tagName,publishedAt')
    .map(r => ({ ...r, repo })))
  .sort((a, b) => b.publishedAt.localeCompare(a.publishedAt))
  .slice(0, LIMIT)
if (releases.length === 0) throw new Error(`No public releases found in ${ORG}`)

const rows = releases.map(r =>
  `| ${r.publishedAt.slice(0, 10)} | [${r.name || r.tagName}](https://github.com/${ORG}/${r.repo}/releases/tag/${encodeURIComponent(r.tagName)}) | \`${r.repo}\` |`)
const body = ['| Date | Release | Repository |', '| :--- | :--- | :--- |', ...rows].join('\n')

const s = readFileSync(file, 'utf8')
const re = /(<!-- releases:start -->)[\s\S]*?(<!-- releases:end -->)/
if (!re.test(s)) throw new Error(`Missing <!-- releases:start/end --> markers in ${file}`)
writeFileSync(file, s.replace(re, `$1\n${body}\n$2`))
console.log(`releases block: ${releases.length} entries, newest ${releases[0].repo}@${releases[0].tagName}`)
