import axios from 'axios';
import { Component, FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import * as URLCONFIG from "../../../URLCONF.json";
import { Chart } from 'react-chartjs-2';
import { Chart as ChartJS, LineController, LineElement, PointElement, LinearScale, Title, CategoryScale} from 'chart.js';
import style from './style.css';

ChartJS.register(LineController, LineElement, PointElement, LinearScale, CategoryScale, Title);

const baseURL = URLCONFIG.BACKEND;

interface CollectionProps {
  contract_address:string
}

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
  volume:string
}

type MapObject = {
  [key:string]: string
}

const Collection:FunctionalComponent<CollectionProps> = (props:CollectionProps) => {
  const { contract_address } = props
  const [data, setData] = useState<CollectionData>();
  const [chart, selectChart] = useState('avg_price');

  const fetchData = useCallback(() => {
    axios.get<CollectionData>(`${baseURL}/nft/collection/${contract_address}`)
      .then((res) => {

        setData(res.data);
        console.log(res.data);
      })
  }, []);

  useEffect(() => {
    console.log('Hello');
    fetchData();
  }, []);

  const chartValue = (dP:DataPoint) => {
    let dict:MapObject = {
      "avg_price": dP.prc.avg,
      "max_price": dP.prc.max,
      "min_price": dP.prc.min,
      "total_minted": dP.tkn.totalMinted,
      "total_burned": dP.tkn.totalBurned,
      "sales_count": dP.vol.count,
      "sales_volume": dP.vol.volume
    }
    return dict[chart];
  };

  const renderChart = () => {
    return (
      <Chart
        type='line'
        data={{
          labels: data?.dataPoints.map((dP) => dP.timestamp),
          datasets: [
            {
              label: chart,
              data: data?.dataPoints.map((dP) => chartValue(dP)),
              borderColor: "red",
              backgroundColor:"white"
            },
          ]
        }}
        options={{
          responsive: true,
          backgroundColor: "red"
        }}

      />
    );
  }

  useEffect(() => {
    renderChart();
  }, [chart])

  const chartOptions = ["avg_price", "max_price", "min_price", "total_minted", "total_burned", "sales_count", "sales_volume"];


  return (
    <div class={style.collection}>
      <div class="collection-left">
        <img class={style.artwork} src={data?.artwork}></img>
        <h1><strong>Collection: </strong>{data?.name}</h1>
        <h3><strong>Address: </strong><a href={`http://etherscan.io/address/${data?.address}`}>{data?.address}</a></h3>
        <h4><strong>Owners: </strong>{data?.owners}</h4>
        <h4><strong>Total Minted: </strong>{data?.total_minted}</h4>
        <h4><strong>Total Burned: </strong>{data?.total_burned}</h4>
      </div>
      <div class="collection-right">
        <select value={chart} onChange={(e:any) => selectChart(e.target.value)}>
          {chartOptions.map((opt:string) => {
            return <option value={opt}>{opt.split("_").map((opt:string) => `${opt.charAt(0).toUpperCase()}${opt.substring(1)}`).join(" ")}</option>
          })}
        </select>
        {renderChart()}
      </div>
    </div>
  );
}


export default Collection;
