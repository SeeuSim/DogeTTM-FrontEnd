import axios from 'axios';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import { Link } from 'preact-router/match';
import * as URLCONF from "../../../../URLCONF.json";
import style from "./style.css";

const baseURL = URLCONF.BACKEND;

type Rank = {
  artwork:string,
  artwork_type:string,
  collection_name:string,
  data:string,
  address:string
};

type RankResponse = {
  data: Rank[]
};

const Ranking: FunctionalComponent = () => {
  const [metric, setMetric] = useState('avg_price');
  const [timePeriod, setTime] = useState('7d');
  const [tableData, setTableData] = useState<Rank[]>();

  const fetchData = useCallback(() => {
    axios.get<RankResponse>(`${baseURL}/nft/dashboard_ranking/${metric}/${timePeriod}`)
      .then((response) => {
        setTableData(response.data.data);
      })
    }, [metric, timePeriod]
  );

  useEffect(
    () => {
      fetchData();
    }, [metric, timePeriod]
  );

  const display = (tableData:Rank[]|undefined) => {
    if (tableData) {
      const priceFormatter = (data:string) => {
        return metric != 'sales_count'
          ? parseFloat(data).toFixed(3)
          : parseInt(data);
      };
      const headersFormatter = (header:string) => {
        header = header.split("_")
                      .map((part:string) => part.charAt(0).toUpperCase() + part.substring(1))
                      .join(" ")
        return metric != "sales_count"
          ? `${header} (ETH)`
          : header;
      };
      const headers = ['Artwork', 'Collection Name', headersFormatter(metric)].map(
        (header:string) => <th class={style.rankHeader}>{header}</th>
      );

      return (
        <table class={style.RankTable}>
          <thead>
            <tr>{headers}</tr>
          </thead>
          <tbody>
          {tableData.map<h.JSX.Element>(
            (elem:Rank) =>
              <tr>
                <td>
                  <img class={style.TableImage} src={elem.artwork}></img>
                </td>
                <td><Link href={`/collections/${elem.address}`}>{elem.collection_name
                                                                  ? elem.collection_name
                                                                  : "<Collection Name>"}</Link></td>
                <td>{priceFormatter(elem.data)}</td>
              </tr>
            )
          }
          </tbody>
        </table>
      );
    } else {
      return <div>Loading</div>;
    }
  }

  return(
    <div>
      <select value={metric} onChange={(e:any) => setMetric(e.target.value)}>
        <option value="avg_price">Average Price</option>
        <option value="max_price">Maximum Price</option>
        <option value="sales_count">Sales Count</option>
        <option value="sales_volume">Sales Volume</option>
      </select>
      <select value={timePeriod} onChange={(e:any) => setTime(e.target.value)}>
        <option value="1d">1 Day</option>
        <option value="7d">7 Days</option>
      </select>
      {display(tableData)}
    </div>
  );
}

export default Ranking;
