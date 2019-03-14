# frozen_string_literal: true

require "arachnid2"

URL = "https://nekdo.ru/"
SPIDER = Arachnid2.new(URL)
MAX_URLS = 100
DOCS_DIR = "docs/raw/"
LINKS_DIR = "docs/links/"
PATH_REGEXP = %r{^\/.*$}.freeze

# documents crawling
responses = []

puts "Start crawling..."

SPIDER.crawl(max_urls: MAX_URLS) { |response| responses << response }

puts <<~INFO
  "#{responses.size} docs crawled.
  Docs directory: #{DOCS_DIR}
  Links directory: #{LINKS_DIR}"
INFO

# documents links storing
links = responses.map(&:effective_url)
File.open("index.txt", "w") { |f| f.puts links }

# creation of directories for downloaded docs and links
Dir.mkdir DOCS_DIR unless File.exist? DOCS_DIR
Dir.mkdir LINKS_DIR unless File.exist? LINKS_DIR

# docs content retrieving and storing
responses.each.with_index(1) do |response, index|
  html_doc = Nokogiri::HTML(response.body)
  html_doc.search("//style|//script").remove

  inner_contents = html_doc.xpath("//text()").map do |content|
    content.text.scan(/[a-zа-я]+/i)
  end

  links = html_doc.xpath("//a").map do |el|
    el["href"] if el["href"].match?(PATH_REGEXP)
  end

  links.compact!

  File.open("#{DOCS_DIR}#{index}.txt", "w") do |f|
    f.puts inner_contents.reject(&:empty?).join(" ").strip
  end

  File.open("#{LINKS_DIR}#{index}.txt", "w") do |f|
    f.puts links.join(" ").strip
  end
end
