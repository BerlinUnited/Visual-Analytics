from vaapi.client import Vaapi
import os, inspect

client = Vaapi(base_url=os.environ["VAT_API_URL"],
               api_key =os.environ["VAT_API_TOKEN"])

# Everything that looks like an endpoint – i.e. has .list() or .filter()
resources = sorted(
    name for name in dir(client)
    if not name.startswith("_")            # skip internals
    and any(hasattr(getattr(client, name), m) for m in ("list", "filter"))
)

print("VA‑API resources:")
for r in resources:
    meths = [m for m in ("list", "filter", "get_single", "create")
             if hasattr(getattr(client, r), m)]
    print(f"  {r:30}  →  {', '.join(meths)}")


# OUTPUT:
# VA‑API resources:
#   accelerometerdata               →  list, create
#   annotations                     →  list, create
#   audiodata                       →  list, create
#   ballcandidates                  →  list, create
#   ballcandidatestop               →  list, create
#   ballmodel                       →  list, create
#   behavior_frame_option           →  list, filter, create
#   behavior_option                 →  list, create
#   behavior_option_state           →  list, create
#   buttondata                      →  list, create
#   cameramatrix                    →  list, create
#   cameramatrixtop                 →  list, create
#   cognitionframe                  →  list, create
#   events                          →  list, create
#   experiment                      →  list, create
#   fieldpercept                    →  list, create
#   fieldpercepttop                 →  list, create
#   frame_filter                    →  list, create
#   fsrdata                         →  list, create
#   games                           →  list, create
#   goalpercept                     →  list, create
#   goalpercepttop                  →  list, create
#   gyrometerdata                   →  list, create
#   image                           →  list, create
#   imudata                         →  list, create
#   inertialsensordata              →  list, create
#   log_status                      →  list, create
#   logs                            →  list, create
#   motionframe                     →  list, create
#   motionstatus                    →  list, create
#   motorjointdata                  →  list, create
#   multiballpercept                →  list, create
#   odometrydata                    →  list, create
#   ransaccirclepercept2018         →  list, create
#   ransaclinepercept               →  list, create
#   robotinfo                       →  list, create
#   scanlineedgelpercept            →  list, create
#   scanlineedgelpercepttop         →  list, create
#   sensorjointdata                 →  list, create
#   shortlinepercept                →  list, create
#   teammessagedecision             →  list, create
#   teamstate                       →  list, create
#   whistlepercept                  →  list, create
#   xabsl_symbol_complete           →  list, create
#   xabsl_symbol_sparse             →  list, create