# -*- encoding: utf-8 -*-
# stub: addressable 2.3.6 ruby lib

Gem::Specification.new do |s|
  s.name = "addressable".freeze
  s.version = "2.3.6"

  s.required_rubygems_version = Gem::Requirement.new(">= 0".freeze) if s.respond_to? :required_rubygems_version=
  s.require_paths = ["lib".freeze]
  s.authors = ["Bob Aman".freeze]
  s.date = "2014-03-24"
  s.description = "Addressable is a replacement for the URI implementation that is part of\nRuby's standard library. It more closely conforms to the relevant RFCs and\nadds support for IRIs and URI templates.\n".freeze
  s.email = "bob@sporkmonger.com".freeze
  s.extra_rdoc_files = ["README.md".freeze]
  s.files = ["README.md".freeze]
  s.homepage = "http://addressable.rubyforge.org/".freeze
  s.licenses = ["Apache License 2.0".freeze]
  s.rdoc_options = ["--main".freeze, "README.md".freeze]
  s.rubyforge_project = "addressable".freeze
  s.rubygems_version = "2.6.7".freeze
  s.summary = "URI Implementation".freeze

  s.installed_by_version = "2.6.7" if s.respond_to? :installed_by_version

  if s.respond_to? :specification_version then
    s.specification_version = 4

    if Gem::Version.new(Gem::VERSION) >= Gem::Version.new('1.2.0') then
      s.add_development_dependency(%q<rake>.freeze, [">= 0.7.3"])
      s.add_development_dependency(%q<rspec>.freeze, [">= 2.9.0"])
      s.add_development_dependency(%q<launchy>.freeze, [">= 0.3.2"])
    else
      s.add_dependency(%q<rake>.freeze, [">= 0.7.3"])
      s.add_dependency(%q<rspec>.freeze, [">= 2.9.0"])
      s.add_dependency(%q<launchy>.freeze, [">= 0.3.2"])
    end
  else
    s.add_dependency(%q<rake>.freeze, [">= 0.7.3"])
    s.add_dependency(%q<rspec>.freeze, [">= 2.9.0"])
    s.add_dependency(%q<launchy>.freeze, [">= 0.3.2"])
  end
end
