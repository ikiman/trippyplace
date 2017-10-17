FROM ruby:2.4.2-alpine

COPY Gemfile /bot/

WORKDIR /bot

RUN bundle install

COPY ./bot.rb /bot

CMD ["ruby", "bot.rb"]
