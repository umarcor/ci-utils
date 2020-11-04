#!/usr/bin/env python3

from github import Github
from os import environ
from pathlib import Path
from subprocess import check_call
from sys import stdout
from tabulate import tabulate

data = []

for repo in Github(environ['INPUT_TOKEN']).get_organization("antmicro").get_repos(
    type='sources',
    sort='pushed',
    direction='desc'
):
    print('::group::%s [%i]' % (repo.name, repo.size))

    if repo.archived or repo.fork or repo.private or repo.size == 0:
        print('Skipping...')
        print('::endgroup::')
        stdout.flush()
        continue

    archive = 'https://codeload.github.com/%s/tar.gz/%s' % (repo.full_name, repo.default_branch)

    print('·', repo.full_name)
    print('  %s' % archive)
    stdout.flush()

    check_call(['curl', '-fsSLo', '%s.tgz' % repo.name, archive])
    check_call(['mkdir', '-p', repo.name])
    check_call(['tar', '-xzf', '%s.tgz' % repo.name, '-C', repo.name, '--strip-components', '1'])
    check_call(['ls', '-lah', repo.name])

    print('::endgroup::')
    stdout.flush()

    root = Path(repo.name)

    data += [[
        'Yes' if (root / '.github' / 'workflows').exists() else '',
        'Yes' if (root / '.travis.yml').exists() else '',
        'https://github.com/%s' % repo.full_name
    ]]

print(tabulate(
    data,
    headers=['GitHub Actions', 'Travis CI', 'Repo'],
    stralign='center',
))
