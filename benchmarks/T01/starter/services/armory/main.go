package main
import ("encoding/json"; "net/http"; "os"; "time")
func main() {
 if len(os.Args)>1 && os.Args[1]=="--healthcheck" { c:=http.Client{Timeout:time.Second}; r,e:=c.Get("http://localhost:8001/health"); if e!=nil { os.Exit(1) }; r.Body.Close(); if r.StatusCode!=200 { os.Exit(1) }; return }
 http.HandleFunc("/health",func(w http.ResponseWriter,r *http.Request){w.Header().Set("Content-Type","application/json"); json.NewEncoder(w).Encode(map[string]string{"status":"ok","service":"armory"})})
 if e:=http.ListenAndServe(":8001",nil); e!=nil { panic(e) }
}
