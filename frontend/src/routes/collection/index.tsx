import axios from 'axios';
import { FunctionalComponent, h } from "preact";
import { useCallback, useEffect, useState } from "preact/hooks";
import * as URLCONFIG from "../../../URLCONF.json";
import PriceGraph from '../../components/Graphs/Price';
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
      .then((res) => setData(res.data))
  }, []);

  useEffect(() => {
    fetchData();
  }, [])
  return <div></div>
}

export default Collection;
