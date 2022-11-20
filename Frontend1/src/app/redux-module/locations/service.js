import axios from "axios";

export const getListTinhThanh = () => {
    return new Promise((resolve, reject) => {
        axios
            // .get(api.API_TINH_THANH)
            .get("https://cchn-v2-api.yte360.com/api/v2/danhmuc/location/tinh-thanh/get-all")
            .then(({ data }) => {
                const resultsTinhThanh = data?.results;
                resultsTinhThanh.forEach((e) => {
                    e.label = e.ten;
                    e.value = e.id;
                })
                resolve(resultsTinhThanh);
            })
            .catch((error) => {
                reject(error)
            })
            .finally(() => { });
    });
}


export const getListQuanHuyen = (value) => {
    return new Promise((resolve, reject) => {
        axios
            .get("https://cchn-v2-api.yte360.com/api/v2/danhmuc/location/quan-huyen/get-all/" + value?.id + "?per_page=100")
            // .get(`${api.API_QUAN_HUYEN + "/get-all"}/${value.id}`)
            .then(({ data }) => {
                const resultsQuanHuyen = data?.results;
                resultsQuanHuyen.forEach((e) => {
                    e.label = e.ten;
                    e.value = e.id;
                });
                resolve({results: resultsQuanHuyen, loai: value.loai})
            })
            .catch((error) => {
                reject(error);
            });
    })
}

export const getListXaPhuong = (value) => {
    return new Promise((resolve, reject) => {
        axios
            .get("https://cchn-v2-api.yte360.com/api/v2/danhmuc/location/xa-phuong/get-all/" + value?.id + "?per_page=100")
            // .get(`${api.API_XA_PHUONG + "/get-all"}/${value.id}`)
            .then(({ data }) => {
                const resultsXaPhuong = data?.results;
                resultsXaPhuong.forEach((e) => {
                    e.label = e.ten;
                    e.value = e.id;
                });
                resolve({ results: resultsXaPhuong, loai: value.loai });
            })
            .catch((error) => {
                reject(error);
            });
    })
}

export const getCATinhThanh = () => {
    return new Promise((resolve, reject) => {
    axios
        .get("https://cchn-v2-api.yte360.com/api/v2/danhmuc/location/CA-tinh-thanh")
        // .get(api.API_CA_TINH_THANH)
        .then(async ({ data }) => {
            resolve(data?.results);

        })
        .catch((error) => {
            reject(error);
        })
    })
}