# Weather report

This is a simple function that uses query.yahooapis.com to retrieve the weather for a specific location.

## Launch the function

```
kubeless function deploy weather --runtime nodejs8 \
  --from-file handler.js \
  --dependencies package.json \
  --handler handler.weather
```

## Execute the function

```
$ kubeless function call weather --data '{"location": "nome, ak"}'
It is -5 celsius degrees in nome, ak and Snow
```

## Delete the function

```
kubeless function delete weather
```
