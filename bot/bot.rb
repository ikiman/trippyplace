require 'telegram/bot'
require 'open-uri'
require 'faraday'
require 'json'

$token = ENV['TELEGRAM_TOKEN']
$stdout.sync = true

# Govno mocha
class CategoriesDetector
  attr_reader :photo

  def initialize(photo, api)
    @photo = photo
    @api = api
  end

  def response
    @response ||= JSON.parse(detector_response.body)
  end

  def detect
    response.inject('') do |result, (k,v)|
      result += "*#{k.capitalize}*: #{v.map(&:capitalize).join(', ')}\n"
      result
    end.gsub(/_/, ' ').gsub(/\//, ' or ')
  end

  def path
    @api.get_file(file_id: id)['result']['file_path']
  end

  def data
    open("https://api.telegram.org/file/bot#{$token}/#{path}").read
  end

  def detector_response
    conn.post do |req|
      req.url '/'
      req.headers['Content-Length'] = size
      req.body = data
    end
  end

  def conn
    Faraday.new(url: 'http://network:8000') do |faraday|
      faraday.adapter Faraday.default_adapter
    end
  end

  def id
    photo.file_id
  end

  def size
    photo.file_size.to_s
  end
end

Telegram::Bot::Client.run($token, logger: Logger.new($stdout)) do |bot|
  bot.listen do |message|
    begin
      if !message.photo.empty?
        photo = message.photo.last
        detector = CategoriesDetector.new(photo, bot.api)
        bot.api.send_message(chat_id: message.chat.id, text: detector.detect, parse_mode: 'Markdown')
      elsif message.text == 'как тебе мой хуй?'
        bot.api.send_message(chat_id: message.chat.id,
                             text: 'ну такое... маловат')
      elsif message.text == 'риал ток'
        bot.api.send_message(chat_id: message.chat.id,
                             text: 'ееее бой')
      else
        bot.api.send_message(chat_id: message.chat.id,
                             text: 'Не умею такого :(')
      end
    rescue => e
      puts "Error: #{e}"
    end
  end
end
