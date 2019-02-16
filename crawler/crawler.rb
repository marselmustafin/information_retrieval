# frozen_string_literal: true

require "arachnid2"

URL = "https://nekdo.ru/"
SPIDER = Arachnid2.new(URL)
MAX_URLS = 100
DOCS_DIR = "docs/raw/"

# documents crawling
responses = []
SPIDER.crawl(max_urls: MAX_URLS) { |response| responses << response }

# documents links storing
links = responses.map(&:effective_url)
File.open("index.txt", "w") { |f| f.puts links }

# creation of directory for downloaded docs
Dir.mkdir DOCS_DIR unless File.exist? DOCS_DIR

# docs content retrieving and storing
responses.each.with_index(1) do |response, index|
  doc = Nokogiri::HTML(response.body)
  doc.search("//style|//script").remove

  File.open("#{DOCS_DIR}#{index}.txt", "w") { |f| f.puts doc.content }
end
