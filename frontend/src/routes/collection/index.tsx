import axios from 'axios';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import * as URLCONFIG from "../../../URLCONF.json";
import { Line } from 'react-chartjs-2';
import style from './style.css';

const baseURL = URLCONFIG.BACKEND;

type CollectionProps = {
  address:string
};

type CollectionData = {
  name:string,
  address:string,
  owners:string,
  total_minted:string,
  total_burned:string,
  artwork:string,
  dataPoints:DataPoint[]
}

type DataPoint = {
  timestamp:string,
  prc:DataPoint_prc,
  tkn:DataPoint_tkn,
  vol:DataPoint_vol
}

type DataPoint_prc = {
  min:string,
  max:string,
  avg:string
}

type DataPoint_tkn = {
  minted:string,
  burned:string,
  totalMinted:string,
  totalBurned:string
}

type DataPoint_vol = {
  count:string,
  vol:string
}

const Collection:FunctionalComponent<CollectionProps> = (props:CollectionProps) => {
  const {address} = props;
  const [data, setData] = useState<CollectionData>();

  const fetchData = useCallback(() => {
    axios.get<CollectionData>(`${baseURL}/nft/collection/${address}`)
      .then((res) => {
        setData(res.data);
        console.log(res.data);
      })
  }, []);

  useEffect(() => {
    fetchData();
  }, []);

  return (
    <div class={style.collection}>
      <div class="collection-left">
        <img src={data?.artwork}></img>
        <h1><strong>Collection: </strong>{data?.name}</h1>
        <h3><strong>Address: </strong>{data?.address}</h3>
        <h4><strong>Owners: </strong>{data?.owners}</h4>
        <h4><strong>Total Minted: </strong>{data?.total_minted}</h4>
        <h4><strong>Total Burned: </strong>{data?.total_burned}</h4>
      </div>
      <div class="collection-right">
        <Line
          data = {{
            labels: data?.dataPoints.map((datapoint:DataPoint) => datapoint.timestamp),
            datasets: [
              {
                label: "Avg Price",
                data: data?.dataPoints.map((datapoint:DataPoint)=>datapoint.prc.avg),
              },
              {
                label: "Max Price",
                data: data?.dataPoints.map((datapoint:DataPoint) => datapoint.prc.max)
              }
            ],
          }}
        />
      </div>
    </div>
  );
}
export default Collection;
