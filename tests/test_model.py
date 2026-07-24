import re

import pytest

from model.project import GITHUB_REGEX, Project


@pytest.mark.parametrize('url', [
    'https://youtu.be/dQw4w9WgXcQ',
    'https://www.youtube.com/watch?v=dQw4w9WgXcQ',
    'https://youtube.com/watch?v=dQw4w9WgXcQ&t=42',
    'https://youtu.be/dQw4w9WgXcQ?si=abc',
])
def test_set_youtube_normalises_any_link_format_to_video_id(url):
    project = Project()
    project.set_youtube(url)
    assert project.youtube == 'dQw4w9WgXcQ'


def test_get_youtube_round_trips():
    project = Project()
    project.set_youtube('https://www.youtube.com/watch?v=dQw4w9WgXcQ')
    assert project.get_youtube() == 'https://youtu.be/dQw4w9WgXcQ'


@pytest.mark.parametrize('url', ['', None, 'https://example.com/video', 'not-a-url'])
def test_set_youtube_raises_on_unparsable_link(url):
    # Раньше здесь падал невнятный TypeError из-за индексации None
    with pytest.raises(ValueError):
        Project().set_youtube(url)


@pytest.mark.parametrize('url', [
    'https://github.com/spytcr/ProjectsCloud',
    'https://github.com/facebook/react-native',
    'https://github.com/vuejs/core.js',
    'https://github.com/user/repo/',
])
def test_github_regex_accepts_real_repository_urls(url):
    assert re.match(GITHUB_REGEX, url)


@pytest.mark.parametrize('url', [
    'https://github.com//',
    'https://github.com/a/b/../../evil',
    'https://github.com/onlyowner',
    'https://evil.com/user/repo',
    'http://github.com/user/repo',
])
def test_github_regex_rejects_malformed_urls(url):
    assert not re.match(GITHUB_REGEX, url)


def test_password_is_hashed_and_verifiable(make_user):
    user = make_user(password='correct-horse')
    assert user.hashed_password != 'correct-horse'
    assert user.check_password('correct-horse')
    assert not user.check_password('wrong')
