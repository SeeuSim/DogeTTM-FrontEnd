import { FunctionalComponent, h } from "preact";
import { useState, useRef, useEffect, useCallback } from "preact/hooks";
import { route } from "preact-router";
import axios from 'axios';
import * as URLCONF from "../../../URLCONF.json";
import style from "./style.css";

const baseURL = URLCONF.BACKEND;

type SearchResult = {
  data: SearchResultEntry[]
}

type SearchResultEntry = {
  name: string,
  address: string,
}

const Searchbar:FunctionalComponent = () => {
  const [options, setOptions] = useState<SearchResultEntry[]>([]);
  const [displayOptions, setDisplayOptions] = useState<SearchResultEntry[]>([]);
  const [searchBy, setSearchBy] = useState("name");
  const [searchParam, setSearchParam] = useState("");

  // Fetching data for dropdown
  const fetchData = useCallback(() => {
    axios.get<SearchResult>(`${baseURL}/nft/search/_all`)
      .then((res) => setOptions(res.data.data));
  }, []);

  useEffect(() => {
    fetchData();
  }, [])
  
  // Handling user interactions
  const ulRef = useRef<HTMLUListElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);

  useEffect(() => {
    inputRef.current?.addEventListener('click', (event:any) => {
      event.stopPropagation();
      if (ulRef.current) {
        ulRef.current.style.display = 'flex';
      }
    });
    document.addEventListener('click', (event:any) => {
      if (ulRef.current) {
        ulRef.current.style.display = 'none';
      }
    });
  }, []);

  const onInputChange = (e: any) => {
    if (!e.target.value) {
      setDisplayOptions([]);
    } else if (e.keyCode == 13){ 
      setSearchParam(e.target.value);
      handleSubmit(e);
    } else {
      setDisplayOptions(optionsFilter(e.target.value));
      setSearchParam(e.target.value);
    }
  }

  const handlePaste = (e: any) => {
    const text_input = e.clipboardData.getData('text');
    if (text_input.length < 5) return;
      setDisplayOptions(optionsFilter(text_input))
  }

  const optionsFilter = (param: string) => {
    return options.filter(
      (option) => {
        return searchBy == "name"
          ? option.name.toLowerCase().startsWith(param.toLowerCase()) || option.name.toLowerCase().includes(param.toLowerCase())
          : option.address.startsWith(param);
      }
    );
  }

  const handleSubmit = (e: any) => {
    if (!searchParam) return;
    console.log(searchParam);
    route(`/search/${searchBy}/${searchParam}`);
  }

  const __route_to = (metric: string, param: string) => {
    route(`/search/${metric}/${param}`)
  }

  return (
    <div className={style.search_field}>
      <input
        id="search-bar"
        type="search"
        placeholder={`Search NFT by `}
        ref={inputRef}
        onKeyUp={onInputChange}
        onPaste={handlePaste}
      />
      <select value={searchBy} onChange={(e: any) => setSearchBy(e.target.value)}>
        <option value="name">Name</option>
        <option value="address">Collection Address</option>
      </select>
      <button type="submit" onClick={handleSubmit}>Search</button>
      <ul
        id="results"
        className="list-group"
        ref={ulRef}>
        {displayOptions?.map(
            (option:SearchResultEntry, index:Number) => {
            return (
              <button
                type="button"
                key={index}
                className="list-group-item list-group-item-action"
                onClick={(e:any) => {
                  if (inputRef.current) {;
                    inputRef.current.value = searchBy == "name"
                      ? option.name
                      : option.address;
                    searchBy == "name" 
                      ? __route_to("name", option.name)
                      : __route_to("address", option.address);
                  }
                }}
                >
                {option.name}
              </button>
            );
        })}
      </ul>
      <div>Break</div>
    </div>
  )
}


export default Searchbar;
