# cricsheets
Process IPL data from cricsheet

## Download data

```bash
python3 main.py -t IPL -d
```

## Build people registry

```bash
python3 main.py -t IPL -p
```

## Build data files
```bash 
python3 main.py -t IPL -b
```

To specify to process only the first n matches (by date)

```bash
python3 main.py -t IPL -b -n <some number>
```
