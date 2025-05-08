# ASSINGMENT 3 (Big Data Analysis)
#### By Dominykas Venclovas, Ugnė Kniukštaitė, Paulina Leščinskaitė
## Database setup

The MongoDB Docker Compose was used to create the database. The setup was sharding, using 10 containers: configuration server, mongos router, and 8 shards. Sharding setup is left as default, based on MMSI value (so all records of one ship stay in one shard). To start the project, having set up Docker and Docker Compose, use the command:
```
docker-compose up -d
```

After that, initiate all shards, use Docker Desktop UI or 'docker exec -it mongos mongosh' in the terminal, then launch this script or initiate each shard individually:
```
rs.initiate({
  _id: "configReplSet",
  configsvr: true,
  members: [{ _id: 0, host: "configsvr:27017" }]
});
 
// each shard's replica set script
var shardNames = ["shard1", "shard2", "shard3", "shard4"];
var ports = [27018, 27019, 27021, 27022];
 
for (let i = 0; i < shardNames.length; i++) {
  rs.initiate({
    _id: `${shardNames[i]}ReplSet`,
    members: [{ _id: 0, host: `${shardNames[i]}:${ports[i]}` }]
  });
}
```
Having done this, add each shard to the database and initiate sharding:
```
sh.addShard("shard1ReplSet/shard1:27018");
sh.addShard("shard2ReplSet/shard2:27019");
sh.addShard("shard3ReplSet/shard3:27021");
sh.addShard("shard4ReplSet/shard4:27022");

sh.enableSharding("ais");
sh.shardCollection("ais.raw_data", { "MMSI": "hashed" });
```

## Adding and filtering data
For this task, one day of ship traffic data is used, available at http://web.ais.dk/aisdata/aisdk-2024-05-01.zip. The data is first sampled randomly based on ship id - MMSI, only 4 million out of 20 million rows are used, to be able to run the project on the local machine in a reasonable amount of time:
```
python preprocess_data.py
```
Later, this sampled data is inserted in parallel to the MongoDB running in Docker containers:
```
python insert_parallel.py
```

After that data should be filtered, removing records with missing essential columns and with MMSI having fewer than 100 records. To do this, first, sharding should be initiated for the new collection of the filtered data in MongoDB:
```
sh.shardCollection("ais.filtered_data", { "MMSI": "hashed" });
```
Then the Python script filtering data in parallel should be launched in Python:

```
python filter_parallel.py
```

## Time delta analysis

To perform time delta analysis in parallel, the user should launch this Python script.
```
python time_calculation.py
```

This script in the code folder will save and plot four histograms of the time differences between two subsequent time points for each vessel.

All histograms have been uploaded to the histograms folder. Each of the four histograms depicts the time delta between subsequent points for each vessel. These histograms have distinct x-axis ranges. The full x-axis range of the histograms is [0, 6000]. However, to gain a better understanding of the main concentration of the time delta, we zoomed in on the x-axis.

### Full range histogram 

In full range histogram plot we can see, that there are 60 000s difference between two subsequent time points at most. However, there are apprx. less than 250 000 time delta of more than 10 000 s.
<img width="600" alt="image" src="https://github.com/user-attachments/assets/e11fa87a-5389-4d53-bd71-9a462bc814b5" />

### Histogram of range 0-1000s

<img width="600" alt="image" src="https://github.com/user-attachments/assets/b2608f3a-9f04-4df6-bfce-8a759af3b3d2" />

### Histogram of range 0-100s

<img width="600" alt="image" src="https://github.com/user-attachments/assets/946c6ebd-2b34-411f-8543-ff39f51f6352" />

### Histogram of range 0-20

<img width="600" alt="image" src="https://github.com/user-attachments/assets/5da6eb58-84e8-43c6-b8cc-de0dd22d261b" />



