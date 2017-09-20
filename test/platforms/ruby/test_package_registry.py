import pytest
import requests

from test import *
from app.platforms.ruby.package_registry import *
from app.dependency import *


@pytest.fixture
def registry(): return RubyPackageRegistry(http_compression=False)


@VCR.use_cassette('ruby_package_registry_version.yaml')
def test_fetch_version(registry):
    version = registry.fetch_version('actionview', '4.1.0')
    assert version.name == 'actionview'
    assert version.number == '4.1.0'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency('actionpack'),
        Dependency('activemodel')
    ]
    assert version.runtime_dependencies == [
        Dependency('activesupport'),
        Dependency('builder'),
        Dependency('erubi'),
        Dependency('rails-dom-testing'),
        Dependency('rails-html-sanitizer')
    ]


@VCR.use_cassette('ruby_package_registry_latest_version.yaml')
def test_fetch_latest_version(registry):
    version = registry.fetch_latest_version('actionview')
    assert version.name == 'actionview'
    assert version.number == '5.1.4'
    assert version.licenses == ['MIT']
    assert version.development_dependencies == [
        Dependency('actionpack'),
        Dependency('activemodel')
    ]
    assert version.runtime_dependencies == [
        Dependency('activesupport'),
        Dependency('builder'),
        Dependency('erubi'),
        Dependency('rails-dom-testing'),
        Dependency('rails-html-sanitizer')
    ]


@VCR.use_cassette('ruby_package_version_name_does_not_exist.yaml')
def test_fetch_version_when_name_does_not_exist(registry):
    with pytest.raises(requests.exceptions.HTTPError):
        registry.fetch_version('foobar666', '666')


@VCR.use_cassette('ruby_package_version_number_does_not_exist.yaml')
def test_fetch_version_when_version_does_not_exist(registry):
    with pytest.raises(Exception) as e:
        registry.fetch_version('rails', '666')
    assert str(e.value) == 'Could not find Ruby gem rails:666'


@VCR.use_cassette('ruby_package_version_name_does_not_exist.yaml')
def test_fetch_latest_version_when_name_does_not_exist(registry):
    with pytest.raises(requests.exceptions.HTTPError):
        registry.fetch_latest_version('foobar666')


@VCR.use_cassette('ruby_package_version_without_license.yaml')
def test_fetch_version_without_license(registry):
    version = registry.fetch_version('coulda', '0.7.1')
    assert version.licenses == []


@VCR.use_cassette('ruby_package_version_without_any_dependencies.yaml')
def test_fetch_version_without_any_dependencies(registry):
    version = registry.fetch_version('rdiscount', '2.2.0.1')
    assert version.runtime_dependencies == []
    assert version.development_dependencies == []


@VCR.use_cassette('ruby_package_version_without_runtime_dependencies.yaml')
def test_fetch_version_without_runtime_dependencies(registry):
    version = registry.fetch_version('bundler', '1.15.4')
    assert version.runtime_dependencies == []
    assert version.development_dependencies == [
        Dependency('automatiek'),
        Dependency('mustache'),
        Dependency('rake'),
        Dependency('rdiscount'),
        Dependency('ronn'),
        Dependency('rspec')
    ]


@VCR.use_cassette('ruby_package_version_without_development_dependencies.yaml')
def test_fetch_version_without_development_dependencies(registry):
    version = registry.fetch_version('rails', '5.1.4')
    assert version.runtime_dependencies == [
        Dependency('actioncable'),
        Dependency('actionmailer'),
        Dependency('actionpack'),
        Dependency('actionview'),
        Dependency('activejob'),
        Dependency('activemodel'),
        Dependency('activerecord'),
        Dependency('activesupport'),
        Dependency('bundler'),
        Dependency('railties'),
        Dependency('sprockets-rails')
    ]
    assert version.development_dependencies == []
