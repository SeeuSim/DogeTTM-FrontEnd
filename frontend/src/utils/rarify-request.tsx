import axios from 'axios';

const API_KEY:string = '1959b00b-435b-4c27-a1b7-66168414d0dc';

async function dashboardData(ranking_method:string, limit:number) {

    let endpoint:string = 'https://api.rarify.tech/data/contracts';
    var params = {
        "include": 'insights',
        "sort": `-insights.${ranking_method}`,
        "page[limit]": limit
    }
    var headers = {
        "Authorization": `Bearer ${API_KEY}`
    }

    const response = await axios.get(endpoint, {params:params, headers:headers}).then((r:any) => {r.data})
    return response;
}

export {dashboardData};
