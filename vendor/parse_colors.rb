require 'rubygems'
require 'nokogiri'
require 'open-uri'

color = ARGV[0]
page = Nokogiri::HTML(open("https://www.color-hex.com/color/" + color))
res = page.css(".fullrow .colordvconline a")
file = File.new('resources/colors/' + color + '.txt', 'w')

for i in (res.length/2-1).downto(1)
	file.write(res[i].text)
end
for i in res.length/2 ... res.length
	file.write(res[i].text)
end 
file.close
