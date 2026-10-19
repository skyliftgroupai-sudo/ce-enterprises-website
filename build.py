#!/usr/bin/env python3
"""Static site generator for C.E. Enterprises Indy Roofing Siding & Restoration LLC.
Run: python3 build.py  -> writes ./public
Add blog posts to POSTS (or posts/*.json) and rebuild; feed.xml + sitemap update automatically."""
import os, json, shutil, html, datetime, glob, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from pages_seo import PAGES
from logo_data import LOGO_B64
LOGO = "data:image/png;base64," + LOGO_B64

_v = os.environ.get("VERCEL_PROJECT_PRODUCTION_URL")
DOMAIN = os.environ.get("SITE_URL") or (f"https://{_v}" if _v else "https://ce-enterprises-indy.vercel.app")  # set SITE_URL once the custom domain is live
BIZ = {
    "name": "C.E. Enterprises Indy Roofing Siding & Restoration LLC",
    "short": "C.E. Enterprises",
    "owner": "Chris Epple",
    "phone": "(317) 402-9681",
    "tel": "+13174029681",
    "email": "epple.chris67@gmail.com",
    "street": "2065 S Kitley Ave",
    "city": "Indianapolis", "state": "IN", "zip": "46203",
    "hours": "Mon–Fri 7:00 AM – 7:00 PM",
    "facebook": "https://www.facebook.com/people/CE-Enterprises/61576991758696/",
    "gmb": "https://share.google/gyH6NSgRT5Bu5YLk9",
}
G = "https://lh3.googleusercontent.com/gps-cs-s/"
P = {  # real photos from the Google Business Profile (owner uploads)
 "showroom": "ANWiy9SSRHVl9BkDz0tS7PHV0gRVWxy-SwauMBIUtvd-dbwIFxYRXYpZ8PSunhRKsZuKUim6peuMtiyIpQqPUj6rTBnPDz1XDyTx4GUjZ2Kw1_IU1f9_4CEcW9v97E95vmyxcQ29-P8bUHe0ctWe",
 "kitchen1": "ANWiy9Sy51mfQVDETSl77bdGI7raczQYAkIA9NZb0SAj7qY6yVfO2RPWpXnvmtv3QQ91cDoz8rk63UEQFx6DoQSc3UaHt0Uvu5O3HJs5BxW-kbtg7489ympg1gPYKHeF-TmQUnGfuzomEq1LT7M",
 "bath_vanity": "ANWiy9TsjkehmMb9CrAf_w6UIks7CTTeJC6fpJRsxxbpnEto2GOvg7CtV79ASfDgwzj6XxfaGuSTxR0DjRvcuFDBKO1-bDRBpNiphXh6Ax1AeBIhaX7NpeAMm5uQYMPxuyofUhA9Wpe412Eql5ur",
 "bath_tub_window": "ANWiy9TZfYKAdHHWCeYMwPf_YbngJP8TQsmD46vmtUCf8QEc0rZ7iuoJFaRvZHC05jDouJngJGjo18eZh3eQFaCoOug5miSLIhex20BmIx86xkTIBVZ7Am8mv5AsybQfTfwYPSCtPf-pofu_HJk",
 "shower_dark": "ANWiy9TTLH_49p-zNTaJ6CKghy-kzEfM22W2hV-q6QpsPEYT2KanjIWVrbTY6Ye659fX_7f1ad1ziu8F8xvucW6YngjotnPrK451Is7MNuZvLIOxiQz1brVZDGLCwpqfAjrj2L3xRYxTvi_AjkJI",
 "tub_free": "ANWiy9QxJepZLteFpjeeOrFuTBt7hm9V2XQZfpcrPBxnkzDiEp6eLtp2I7lMguIHrAaDCH4LOv3wSHI3eJMj-q2A2MrHSQU_kFmGSurYGQ87RZqtHlUVnXeG3sJPRDtT10xrLDVH7aw3lwEj6Oef",
 "exterior_patio": "ANWiy9Q2bGpLbVrRPrMVNOV77VCR46OLR3xS1y3tEw4kURjVpDncnvzNxBLTdaTFvzGblvBFJme5xX73yHR_3o2tcIWomEAPHUqwAfl9Ejuylxj7z7HCV3qEg9nwYmAVkJtIxFxGyrnz",
 "reno_progress": "ANWiy9SgvBvqiYbkp5FUIgkfNWcqjDxAZfcLKB8Ji7-fegIa5LoM7jqFzepmL5bB04U217N1T82Pv4mJwNuTbX6htkeGG9Zp8TjmJzU2qutt-hKvxPA3zwL_KG1Xotrv3LXKckKyAWOu",
 "new_build": "ANWiy9Sn4rSCmWgq2gKILHlkgADTmENgSl3HHIFqXD9xfFPoi8HWfhevtLJY9Wj_hwFKr8JFLz-yKq4aaVKhHINYwpOA6PMkT1G631kiDIAZ6z9Y1-hZpBXLIH6rlyo-JRfvUdDu3vu__K2QdUZk",
 "shower_glass": "ANWiy9TW8ulqCw7RTEovYZJ98PuqQgOj88SN4RbWiYhYBbtTkp_IFeBP_N1fJFQ0YYzLG-EMx2W3jH-IqGUd-k6C96zLooQNzcyz4sSXPZMwDzkL874UnGVIfEnCiBuPnUg5UAP5v_aA29cjmvw",
 "roof_cedar": "ANWiy9TMzdH15Rcaj2TepUCFLXwYC7Xfr8ADXlcQgvvBmi5nYiaGqJ3OzgqWNbC_SMiKC71oUneYjJcadD5wpnZM70-KtwNAtKB5yV9CplsgPrKZclF0yrjuum-0aNorNFql3ers0Ub-qFSuhwtb",
 "addition_wrap": "ANWiy9QE0_BOqM6mm4JJLQo2ewRKzHbdvkU1A1_a1pR_LZJMeHL1xEvAvzK0aLrml-DiUDT7fJFrlcj_ez84GRQP08Rgaqb-c1uDgYNf2PI9X7sR2Fgz7a9Yr6db33kEor4joz_Xz99k",
 "kitchen2": "ANWiy9QxKcgailtMrhVHushvmDWM6FWhJtNwbzAeTr2wI_TqUmI7n0M907i_VCBOw3_mjeamslTKWFJkTK7WJ_2l6NpLfBZ2joYjvhkMft9onS-4La-XmxJR8PxLXMlodJBzwPDKo4_lb3VAYcg",
 "bath_wood": "ANWiy9RbMzYa4DkCosw8v7yZohRF3Gg0loNfJZTIrf0XM6wVP8m-C_nmHBuqfcr0L852220oQlSXjJC5bgpl0dmnkORoE5lf5ogRfuHN4LJt8kaKzlJMdname9AVUXeoJ7zcDDWeOlspHdTdFw8q",
 "roof_slate": "ANWiy9T-w3Q5EurDxPaeEpvq4ziweseKehR1ZaChqZGjRtZfVYFINHAQDF0eFQb2Di7Ccm1Buviic57lA8prV6mBDpppxbap3_o700x2dIrQeQaZhI5MQYIKOjf0P7mER4jjDgawz_GLsP7ZtSbZ",
 "bath_lit": "ANWiy9TDi7yCI-Grsc4c6X1Xr2mmDFh174IODAz6sq5waI6zDq6-ByMIISH5si-J3Hdyxb4r1QpwzG25Vu98l3SNLvVuA1N6MRwJx2wWoSwcWyf9imoaMUZqIOEz2PMFe6yGIj1uMpAzHHrOGPI",
 "bath_marble": "ANWiy9QoBJpBZOIQwut74_aquFq5A1a2yENrgKI6v03JDNrQFEymzFegjRTPKMP2PKy36aGKdoNVLKYzfYce3wstFC3jddUO7YyKhVBHHU3-ch9KGMn0-4TwiLu6DryWBtR6OhSbCX44PXpP16Y",
 "bath_white": "ANWiy9QHUECSa_oQW5V-6op6ZM53ymcFR84ZFjUprwrSqUAwRHpuID22hNYNqzhsCue0gfvETCPbRCTvu19JQ5RoWjTSR3mGo3fllbJhw1dFr_hHp9s9C_XBgvXR71ysZihOQuw16QF6SRlZG_o",
 "framing": "ANWiy9Tccfz2g9dzfWmS2QrNgeDl3EBVvVlTW_LPrGl8jn3gojBKikE-rcJvBJWipTQYutFafTsl6I4Ya5hRV0kcNknWa15oDjSwjSB5S0VKJFin9LG_VAl52BGBZELKaF9w7o0PA0e6Ow",
}
def img(k, w=1400): return f"/p/{k}-{w}.jpg"
def imgabs(k, w=1200): return f"{G}{P[k]}=w{w}"
e = html.escape

CITIES = [
 {"slug":"indianapolis","name":"Indianapolis","note":"From Fountain Square and Garfield Park to Irvington and Broad Ripple, our shop on S Kitley Ave puts us minutes from most Indianapolis neighborhoods."},
 {"slug":"greenwood","name":"Greenwood","note":"Greenwood homeowners get the same crew and the same owner on site — a short drive down I-65 from our Indianapolis shop."},
 {"slug":"westfield","name":"Westfield","note":"Westfield's newer subdivisions and established homes alike see roof, siding and addition work from our team on the north side."},
 {"slug":"noblesville","name":"Noblesville","note":"We serve Noblesville and the rest of Hamilton County with roofing, siding and remodeling for homes and commercial buildings."},
 {"slug":"avon","name":"Avon","note":"West of the city in Hendricks County, Avon homeowners call us for storm repairs, re-roofs, siding and room additions."},
]

SERVICES = [
 {"slug":"roofing","nav":"Roofing","h1":"Roofing Contractor in Indianapolis, IN","kw":"roofing contractor","photo":"roof_cedar",
  "title":"Roofing Contractor Indianapolis IN | Roof Repair & Replacement | C.E. Enterprises",
  "desc":"Residential & commercial roofing in Indianapolis, Greenwood, Westfield, Noblesville & Avon. Roof repair, replacement, inspections, storm damage. Call (317) 402-9681.",
  "intro":"Roof repair, roof replacement and new roof installation for homes and commercial buildings across the Indianapolis metro. Chris Epple and his crew handle every part of the job — inspection, tear-off, installation and clean-up — and you deal with the owner, not a call center.",
  "subs":[("Roof Inspection","Residential and commercial roof inspections that document what you actually have: shingle condition, flashing, vents, decking soft spots and leak points. You get a straight answer on repair versus replacement."),
          ("Roof Repair","Leaks, missing shingles, failed flashing, chimney and skylight leaks. Our reviews mention flashing fixes and leak calls specifically — small jobs get the same care as big ones."),
          ("Roof Replacement & Re-Roofing","Full tear-off and replacement or re-roofing when the deck is sound. We walk you through materials, ventilation and timeline before work starts."),
          ("Storm Damage & Emergency Roofing","Wind, hail and fallen-limb damage. We tarp and secure the roof fast, then document the damage so you have what you need for your insurance conversation."),
          ("Shingle Roofs","Architectural asphalt shingle roofs for residential and light commercial buildings — the most common roof in central Indiana."),
          ("Metal Roofs","Standing seam and exposed-fastener metal roofing for homes, garages, barns and commercial buildings."),
          ("Rubber (EPDM) & Flat Roofs","Rubber roof repair and replacement for low-slope and flat roofs on additions, porches and commercial buildings."),
          ("Tile & Specialty Roofs","Tile, slate, cedar and specialty roofing — including copper and detail work on historic homes.")],
 },
 {"slug":"siding","nav":"Siding","h1":"Siding Company & Siding Installation in Indianapolis","kw":"siding contractor","photo":"new_build",
  "title":"Siding Company & Siding Installation Indianapolis IN | C.E. Enterprises",
  "desc":"Siding installation, replacement and repair in Indianapolis and surrounding cities. Residential & commercial. Owner-operated. Call (317) 402-9681 for a free estimate.",
  "intro":"New siding protects the house and changes how it looks from the street. We install and replace siding on homes, additions and commercial buildings, and we pair it with roofing so the whole exterior is weather-tight at once.",
  "subs":[("Siding Installation","New siding on new construction, home additions and full exterior makeovers."),
          ("Siding Replacement","Tear-off of failing, faded or storm-damaged siding, inspection of the sheathing and house wrap underneath, then new siding and trim."),
          ("Siding Repair","Replacing damaged panels and trim after storms, impact or moisture problems."),
          ("Roofing + Siding Packages","One crew, one schedule, one point of contact for the full exterior — the work our name is built on.")],
 },
 {"slug":"home-additions","nav":"Home Additions","h1":"Home Additions & Room Additions in Indianapolis","kw":"home additions","photo":"addition_wrap",
  "title":"Home Additions Indianapolis IN | Room Addition Contractor | C.E. Enterprises",
  "desc":"Room additions, second stories, bump-outs and garage additions in Indianapolis, Greenwood, Westfield, Noblesville & Avon. Framing to roof to finish. Call (317) 402-9681.",
  "intro":"Need more space without moving? We build room additions from the footings up — framing, roofing, siding and interior finish — so the new space ties into your existing home inside and out. Because roofing and siding are our core trades, the roof line and exterior match the original house.",
  "subs":[("Room Additions","Bedrooms, family rooms, sunrooms and home offices added onto the main floor."),
          ("Primary Suite Additions","A new bedroom and bathroom together — framed, roofed and finished as one project."),
          ("Garage & Bump-Out Additions","Garage additions and smaller bump-outs that add square footage where you need it."),
          ("Addition Roofing","Tying a new roof into an existing one is where additions leak. We frame, flash and shingle the tie-in ourselves.")],
 },
 {"slug":"custom-home-builder","nav":"Custom Homes","h1":"Custom Home Builder in Indianapolis, IN","kw":"custom home builders","photo":"new_build",
  "title":"Custom Home Builders Indianapolis IN | C.E. Enterprises General Contractor",
  "desc":"Custom home building in the Indianapolis metro — framing, roofing, siding and interior finish under one owner-operated general contractor. Call (317) 402-9681.",
  "intro":"We build custom homes as the general contractor from site work through final walkthrough. One owner, one crew, and the same roofing and siding standards we're known for on every exterior.",
  "subs":[("Planning & Budget","We help you turn plans into a realistic scope and schedule before ground is broken."),
          ("Framing & Shell","Framing, sheathing, house wrap, roofing and siding to get the home dried in."),
          ("Interior Finish","Kitchens, baths, flooring and trim — the same crew that does our remodeling work."),
          ("Final Walkthrough","We walk the house with you and close out the punch list before handing over keys.")],
 },
 {"slug":"kitchen-remodeling","nav":"Kitchen Remodeling","h1":"Kitchen Remodeling in Indianapolis, IN","kw":"kitchen remodeling","photo":"kitchen1",
  "title":"Kitchen Remodeling Indianapolis IN | Kitchen Remodel Contractor | C.E. Enterprises",
  "desc":"Kitchen remodels in Indianapolis and surrounding cities — cabinets, countertops, backsplash, flooring and layout changes. Call (317) 402-9681 for a free estimate.",
  "intro":"From cabinet and countertop updates to full layout changes, we remodel kitchens that work the way your family cooks. You'll see real C.E. Enterprises kitchens below — white shaker cabinets, quartz tops, tile backsplash and open layouts.",
  "subs":[("Cabinets & Countertops","New cabinetry, islands and countertop installation."),
          ("Backsplash & Tile","Tile backsplash and accent walls that finish the space."),
          ("Flooring","Durable flooring that runs through the kitchen and adjoining rooms."),
          ("Layout Changes","Opening walls and reworking layouts when the old kitchen just doesn't flow.")],
 },
 {"slug":"bathroom-remodeling","nav":"Bathroom Remodeling","h1":"Bathroom Remodeling in Indianapolis, IN","kw":"bathroom remodeling","photo":"bath_tub_window",
  "title":"Bathroom Remodeling Indianapolis IN | Bathroom Remodel Contractor | C.E. Enterprises",
  "desc":"Bathroom remodels in Indianapolis — walk-in showers, freestanding tubs, double vanities and tile. Owner-operated contractor. Call (317) 402-9681.",
  "intro":"Bathrooms are the room we post most on our Google profile — walk-in glass showers, freestanding tubs, double vanities and floor-to-ceiling tile. Every one is built with proper waterproofing behind the tile, because water problems are what we fix for a living.",
  "subs":[("Walk-In Showers","Frameless glass, tile surrounds, niches and benches."),
          ("Tubs","Freestanding soaking tubs and tub-to-shower conversions."),
          ("Vanities & Lighting","Single and double vanities, mirrors and lighting."),
          ("Tile & Waterproofing","Tile floors and walls over a properly waterproofed substrate.")],
 },
 {"slug":"full-home-renovation","nav":"Full House Renovation","h1":"Full House Renovation in Indianapolis, IN","kw":"home renovation","photo":"showroom",
  "title":"Full House Renovation Indianapolis IN | Whole Home Remodel | C.E. Enterprises",
  "desc":"Whole-house renovations in Indianapolis — roof to basement, inside and out — from one owner-operated general contractor. Call (317) 402-9681.",
  "intro":"Our motto is “from the roof to the street.” For full renovations that means one contractor handling the roof, siding, kitchen, baths, flooring and everything between — residential or commercial.",
  "subs":[("Exterior","Roofing, siding, gutters and water-problem fixes."),
          ("Interior","Kitchens, bathrooms, flooring and open-concept changes."),
          ("Water Problems","Leaks, flashing failures and basement water issues traced to the source and fixed."),
          ("Commercial Buildouts","Renovations for commercial and multi-family properties.")],
 },
]

REVIEWS = [
 ("Donald Armstrong","My roof and siding look brand new, and the attention to detail was impressive. No surprises with pricing."),
 ("Tim Houston","They came out for a roof leak and a basement leak… stopped all my leaks and solved all my issues."),
 ("Nikki Merrick","Helped fix the flashing on my grandparents' house. Gave us a great deal. Straightforward, easy to work with."),
 ("Logan Tarver","Chris and his team are the best roofing contractor in the area. Chris always keeps communication."),
 ("Jeff Asbery","Honest, straightforward, thorough, detailed and a great communicator."),
 ("Leroy Pena","Professional, responsive, and delivered high-quality work on time. Highly recommend."),
]

FAQS = [
 ("What services does C.E. Enterprises offer?","Roofing and siding, home additions, custom home building, kitchen remodeling, bathroom remodeling and full house renovations — for residential and commercial properties."),
 ("What areas do you serve?","We're based at 2065 S Kitley Ave in Indianapolis and serve roughly a 40-mile radius, including Indianapolis, Greenwood, Westfield, Noblesville and Avon."),
 ("Do you handle storm damage and emergency roof repairs?","Yes. Call (317) 402-9681. We secure the roof first, then document the damage so you have photos and a written scope for your insurance conversation."),
 ("Who will I be working with?","C.E. Enterprises is owner-operated. Owner Chris Epple is involved in your project from the estimate to the final walkthrough."),
 ("Are you BBB accredited?","Yes — C.E. Enterprises has been BBB Accredited since December 2019."),
 ("How do I get an estimate?","Call (317) 402-9681, email epple.chris67@gmail.com, or send the form on this page. Estimates are free."),
]

POSTS = [
 {"slug":"roof-repair-vs-replacement-indianapolis","date":"2026-10-16",
  "title":"Roof Repair vs. Roof Replacement: How Indianapolis Homeowners Decide",
  "desc":"Not sure whether your roof needs a repair or a full replacement? The signs, the questions to ask, and how Indiana weather factors in — from an Indianapolis roofer.",
  "kw":"roof repair vs replacement","photo":"roof_slate",
  "body":"""
<p>A water stain on the ceiling or a few shingles in the yard after a storm usually leads to one question: can this be fixed, or does the whole roof need to go? The honest answer depends on what is actually happening up there — and that's something a proper inspection answers, not a guess from the driveway.</p>
<p>Here is how we walk Indianapolis homeowners through the decision.</p>
<h2>Start with what failed — and why</h2>
<p>Most leaks are not caused by the whole roof wearing out at once. They come from one weak point: flashing around a chimney or skylight, a cracked pipe boot, nails backing out, or a section of shingles lifted by wind. If the rest of the roof is in good shape, fixing that weak point is usually the right call.</p>
<p>When we inspect, we look at:</p>
<ul>
<li><strong>Flashing</strong> at chimneys, walls, valleys and skylights — the most common leak source we repair.</li>
<li><strong>Shingle condition</strong> across all slopes, not just the damaged one: granule loss, curling, cracking and brittleness.</li>
<li><strong>Decking</strong> — soft or spongy spots mean water has been getting in for a while.</li>
<li><strong>Ventilation</strong> — poor attic ventilation shortens roof life and can cause ice dams in an Indiana winter.</li>
<li><strong>The attic side</strong> — staining, mold or daylight through the boards tell you more than the shingles do.</li>
</ul>
<h2>When a repair makes sense</h2>
<ul>
<li>The damage is limited to one area — a few missing shingles, one bad flashing detail, a single failed vent boot.</li>
<li>The rest of the roof still has good granule coverage and lies flat.</li>
<li>The decking underneath is solid.</li>
<li>The roof has a reasonable amount of life left in it.</li>
</ul>
<p>A good repair should blend in and stop the water. One of our customers put it simply after we fixed the flashing on her grandparents' house: straightforward, easy to work with, and the problem was solved.</p>
<h2>When replacement is the smarter money</h2>
<ul>
<li><strong>Problems are showing up in several places</strong> instead of one.</li>
<li><strong>Shingles are curling, cracking or bald</strong> across most of the roof.</li>
<li><strong>You've already repaired it more than once</strong> in the last few years and it keeps coming back.</li>
<li><strong>The decking is soft</strong> in multiple spots.</li>
<li><strong>Storm damage is widespread</strong> across slopes — common after a major hail or wind event in central Indiana.</li>
</ul>
<p>At that point, repeated repairs tend to cost more over time than a new roof would, and you still have an old roof.</p>
<h2>How Indiana weather changes the math</h2>
<p>Central Indiana roofs deal with summer heat, spring wind and hail storms, and winters that freeze and thaw over and over. That freeze-thaw cycle is hard on a roof that is already letting a little water in: moisture gets under shingles and around flashing, freezes, expands, and makes the gap bigger. A small leak in October can be a much bigger problem by March.</p>
<p>That's why we recommend getting a questionable roof looked at in the fall, before winter, or soon after any major storm.</p>
<h2>What about insurance?</h2>
<p>If the damage came from a storm, your homeowner's policy may cover some or all of it, depending on your coverage. We don't make promises about what your insurer will pay — but we do document the damage with photos and a written scope so you have clear information for your adjuster.</p>
<h2>Questions to ask any roofer</h2>
<ul>
<li>Did you go on the roof and in the attic, or just look from the ground?</li>
<li>Can you show me photos of the damage?</li>
<li>Is this repairable, and how long should the repair last?</li>
<li>If you recommend replacement, what specifically makes a repair the wrong choice?</li>
<li>Who will be on site, and who do I call with questions?</li>
</ul>
<h2>Get a straight answer on your roof</h2>
<p>C.E. Enterprises is an owner-operated roofing, siding and remodeling contractor based in Indianapolis and BBB Accredited since 2019. Owner Chris Epple will tell you whether your roof needs a repair or a replacement — and why. We serve Indianapolis, Greenwood, Westfield, Noblesville, Avon and the surrounding area for residential and commercial roofs.</p>
<p><strong>Call <a href="tel:+13174029681">(317) 402-9681</a></strong> or <a href="/#quote">request a free roof inspection</a>.</p>
<p>Related: <a href="/roofing/">Roofing services</a> · <a href="/siding/">Siding</a> · <a href="/roofing-contractor-indianapolis-in/">Roofing in Indianapolis</a></p>
"""},
]

# ---------------- templates ----------------
CSS = open(os.path.join(os.path.dirname(__file__), "style.css")).read()

def nav():
    svc = "".join(f'<li><a href="/{s["slug"]}/">{s["nav"]}</a></li>' for s in SERVICES)
    ct = "".join(f'<li><a href="/roofing-contractor-{c["slug"]}-in/">{c["name"]}, IN</a></li>' for c in CITIES)
    rf = "".join(f'<li><a href="/{p["slug"]}/">{p["nav"]}</a></li>' for p in PAGES if p["slug"]!="general-contractor")
    svc += '<li><a href="/general-contractor/">General Contractor</a></li>'
    return f'''
<div class="topbar"><div class="wrap">
  <span>BBB Accredited since 2019</span><span class="hide-sm">{BIZ["hours"]}</span>
  <a href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a>
</div></div>
<header class="hdr"><div class="wrap hdr-in">
  <a href="/" class="brand" aria-label="C.E. Enterprises home"><img src="{LOGO}" alt="C.E. Enterprises logo" width="64" height="62"><span><b>C.E. Enterprises</b><small>Roofing · Siding · Restoration</small></span></a>
  <input type="checkbox" id="mt" class="mt"><label for="mt" class="burger" aria-label="Menu"><i></i><i></i><i></i></label>
  <nav class="nav"><ul>
    <li><a href="/">Home</a></li>
    <li class="dd"><a href="/roofing/">Roofing</a><ul><li><a href="/roofing/">All Roofing Services</a></li>{rf}</ul></li>
    <li class="dd"><a href="/#services">Services</a><ul>{svc}</ul></li>
    <li class="dd"><a href="/#areas">Service Areas</a><ul>{ct}</ul></li>
    <li><a href="/#work">Our Work</a></li>
    <li><a href="/blog/">Blog</a></li>
    <li><a href="/#quote" class="btn btn-gold">Free Estimate</a></li>
  </ul></nav>
</div></header>'''

def footer():
    svc = "".join(f'<li><a href="/{s["slug"]}/">{s["nav"]}</a></li>' for s in SERVICES)
    ct = "".join(f'<li><a href="/roofing-contractor-{c["slug"]}-in/">Roofing {c["name"]}</a></li>' for c in CITIES)
    rf = "".join(f'<li><a href="/{p["slug"]}/">{p["nav"]}</a></li>' for p in PAGES if p["slug"]!="general-contractor")
    svc += '<li><a href="/general-contractor/">General Contractor</a></li>'
    y = datetime.date.today().year
    return f'''
<section class="cta-band"><div class="wrap"><h2>From the roof to the street — let's talk.</h2><p>Free estimates for residential and commercial projects across the Indianapolis metro.</p>
<a class="btn btn-gold btn-lg" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a></div></section>
<footer class="ftr"><div class="wrap fgrid">
 <div><img src="{LOGO}" alt="" width="90" height="88"><p><b>{e(BIZ["name"])}</b><br>{BIZ["street"]}<br>{BIZ["city"]}, {BIZ["state"]} {BIZ["zip"]}</p>
 <p><a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a><br><a href="mailto:{BIZ["email"]}">{BIZ["email"]}</a></p></div>
 <div><h4>Roofing</h4><ul>{rf}</ul></div>
 <div><h4>Services</h4><ul>{svc}</ul></div>
 <div><h4>Service Areas</h4><ul>{ct}</ul></div>
 <div><h4>Hours</h4><p>Monday – Friday<br>7:00 AM – 7:00 PM<br>Saturday & Sunday: Closed</p>
 <p><a href="{BIZ["facebook"]}" rel="noopener" target="_blank">Facebook</a> · <a href="{BIZ["gmb"]}" rel="noopener" target="_blank">Google</a> · <a href="/blog/">Blog</a></p></div>
</div><div class="wrap copy">© {y} {e(BIZ["name"])}. All rights reserved.</div></footer>
<a class="callfab" href="tel:{BIZ["tel"]}" aria-label="Call {BIZ["phone"]}">📞 Call Now</a>'''

def schema_biz():
    return {
     "@context":"https://schema.org","@type":["RoofingContractor","GeneralContractor"],
     "name":BIZ["name"],"url":DOMAIN+"/","telephone":BIZ["tel"],"email":BIZ["email"],
     "image":imgabs("exterior_patio"),"logo":DOMAIN+"/img/logo.png","founder":{"@type":"Person","name":BIZ["owner"]},
     "address":{"@type":"PostalAddress","streetAddress":BIZ["street"],"addressLocality":BIZ["city"],"addressRegion":BIZ["state"],"postalCode":BIZ["zip"],"addressCountry":"US"},
     "geo":{"@type":"GeoCoordinates","latitude":39.7356,"longitude":-86.1287},
     "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday"],"opens":"07:00","closes":"19:00"}],
     "areaServed":[{"@type":"City","name":f'{c["name"]}, IN'} for c in CITIES],
     "sameAs":[BIZ["facebook"]],
    }

def page(path, title, desc, body, extra_schema=None, og_img=None):
    canon = DOMAIN + path
    schemas = [schema_biz()] + (extra_schema or [])
    ld = "\n".join(f'<script type="application/ld+json">{json.dumps(s)}</script>' for s in schemas)
    doc = f'''<!doctype html><html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{e(title)}</title><meta name="description" content="{e(desc)}">
<link rel="canonical" href="{canon}"><link rel="icon" href="{LOGO}">
<meta property="og:type" content="website"><meta property="og:title" content="{e(title)}"><meta property="og:description" content="{e(desc)}">
<meta property="og:url" content="{canon}"><meta property="og:image" content="{og_img or imgabs('exterior_patio')}"><meta name="twitter:card" content="summary_large_image">
<link rel="alternate" type="application/rss+xml" title="C.E. Enterprises Blog" href="/feed.xml">
<link rel="preconnect" href="https://fonts.googleapis.com"><link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Oswald:wght@500;600;700&family=Inter:wght@400;500;600&display=swap" rel="stylesheet">
<link rel="stylesheet" href="/style.css">{ld}</head><body>{nav()}<main>{body}</main>{footer()}
<script>document.querySelectorAll('.nav a').forEach(a=>a.addEventListener('click',()=>{{document.getElementById('mt').checked=false}}));
document.querySelectorAll('.qform').forEach(function(f){{f.addEventListener('submit',function(ev){{ev.preventDefault();var d=new FormData(f);var b='Name: '+d.get('name')+'%0D%0APhone: '+d.get('phone')+'%0D%0ACity: '+d.get('city')+'%0D%0AService: '+d.get('service')+'%0D%0A%0D%0A'+encodeURIComponent(d.get('msg')||'');location.href='mailto:{BIZ["email"]}?subject='+encodeURIComponent('Estimate request – '+d.get('service'))+'&body='+b;}})}});</script>
</body></html>'''
    out = os.path.join("public", path.strip("/"), "index.html") if path.endswith("/") else os.path.join("public", path.strip("/"))
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w").write(doc)
    return canon

def quote_form(heading="Get Your Free Estimate"):
    opts = "".join(f"<option>{s['nav']}</option>" for s in SERVICES) + "<option>Storm / Emergency Roof Repair</option><option>Commercial Project</option>"
    cts = "".join(f"<option>{c['name']}</option>" for c in CITIES) + "<option>Other (within 40 miles)</option>"
    return f'''<form class="qform"><h3>{heading}</h3>
<input name="name" required placeholder="Full name" aria-label="Full name"><input name="phone" required type="tel" placeholder="Phone" aria-label="Phone">
<select name="city" aria-label="City">{cts}</select><select name="service" aria-label="Service">{opts}</select>
<textarea name="msg" rows="3" placeholder="Tell us about your project" aria-label="Project details"></textarea>
<button class="btn btn-gold" type="submit">Request Estimate</button><p class="fine">Prefer to talk? <a href="tel:{BIZ["tel"]}">{BIZ["phone"]}</a></p></form>'''

def reviews_html():
    cards = "".join(f'<figure class="rev"><div class="stars">★★★★★</div><blockquote>“{e(t)}”</blockquote><figcaption>— {e(n)}, Google review</figcaption></figure>' for n,t in REVIEWS)
    return f'''<section class="sec alt" id="reviews"><div class="wrap"><p class="eyebrow">4.8 ★ on Google · 15 reviews</p><h2>What Our Customers Say</h2><div class="revs">{cards}</div>
<p class="center"><a class="btn btn-outline" href="{BIZ["gmb"]}" target="_blank" rel="noopener">Read all reviews on Google</a></p></div></section>'''

def faq_html(faqs):
    items = "".join(f"<details><summary>{e(q)}</summary><p>{e(a)}</p></details>" for q,a in faqs)
    sch = {"@context":"https://schema.org","@type":"FAQPage","mainEntity":[{"@type":"Question","name":q,"acceptedAnswer":{"@type":"Answer","text":a}} for q,a in faqs]}
    return f'<section class="sec" id="faq"><div class="wrap narrow"><h2>Frequently Asked Questions</h2>{items}</div></section>', sch

# ---------------- pages ----------------
def build_home():
    spec = ["Roofing & Siding","Home Additions","Custom Homes","Kitchen Remodeling","Bathroom Remodeling","Full House Renovation"]
    cards = "".join(f'''<a class="card" href="/{s["slug"]}/"><img src="{img(s["photo"],800)}" alt="{e(s["nav"])} by C.E. Enterprises in Indianapolis" loading="lazy"><div><h3>{s["nav"]}</h3><p>{e(s["intro"][:120].rsplit(" ",1)[0])}…</p><span>Learn more →</span></div></a>''' for s in SERVICES)
    gal_keys = ["exterior_patio","kitchen1","shower_glass","roof_slate","bath_wood","new_build","kitchen2","tub_free","roof_cedar","bath_lit","reno_progress","shower_dark"]
    gal = "".join(f'<img src="{img(k,700)}" alt="C.E. Enterprises project photo" loading="lazy">' for k in gal_keys)
    areas = "".join(f'<a href="/roofing-contractor-{c["slug"]}-in/" class="area"><b>{c["name"]}, IN</b><span>Roofing · Siding · Remodeling</span></a>' for c in CITIES)
    faq, fsch = faq_html(FAQS)
    body = f'''
<section class="hero" style="--bg:url('{img("exterior_patio",1800)}')"><div class="wrap hero-in">
 <div class="hero-copy"><p class="eyebrow light">Indianapolis · Greenwood · Westfield · Noblesville · Avon</p>
 <h1>Indianapolis Roofing, Siding &amp; Home Remodeling Contractor</h1>
 <p class="lead">Owner-operated general contractor for residential and commercial properties. Roofs, siding, room additions, custom homes, kitchens and baths — <em>from the roof to the street.</em></p>
 <div class="hero-cta"><a class="btn btn-gold btn-lg" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a><a class="btn btn-ghost btn-lg" href="#quote">Free Estimate</a></div>
 <ul class="trust"><li>★ 4.8 Google rating</li><li>BBB Accredited since 2019</li><li>Residential &amp; Commercial</li></ul></div>
 {quote_form()}
</div></section>
<section class="strip"><div class="wrap"><h2>Our Team Specializes In</h2><ul>{"".join(f"<li>{x}</li>" for x in spec)}</ul></div></section>
<section class="sec" id="services"><div class="wrap"><p class="eyebrow">What we do</p><h2>Our Services</h2><div class="cards">{cards}</div></div></section>
<section class="sec alt about"><div class="wrap two"><div>
 <p class="eyebrow">About us</p><h2>Owner-Operated. Honest. On Site.</h2>
 <p>C.E. Enterprises Indy Roofing Siding &amp; Restoration LLC is run by owner <b>Chris Epple</b> out of our shop at 2065 S Kitley Ave in Indianapolis. When you call, you talk to the person responsible for your project — and he's the one who shows up to look at it.</p>
 <p>We started with roofs and siding — solving water problems and keeping homes weather-tight — and grew into a full general contractor building room additions, custom homes, kitchens and bathrooms. Customers keep mentioning the same things in their reviews: clear communication, clean job sites and no surprises on price.</p>
 <ul class="checks"><li>BBB Accredited since December 2019</li><li>Residential &amp; commercial work</li><li>Serving a 40-mile radius around Indianapolis</li><li>Free estimates</li></ul>
 <a class="btn btn-green" href="tel:{BIZ["tel"]}">Talk With Chris</a></div>
 <div class="stack"><img src="{img("kitchen2",900)}" alt="Kitchen remodel with island by C.E. Enterprises" loading="lazy"><img src="{img("bath_vanity",700)}" alt="Double vanity bathroom remodel in Indianapolis" loading="lazy"></div></div></section>
<section class="sec additions"><div class="wrap two rev-order"><div>
 <p class="eyebrow">Room additions</p><h2>Home Additions Built From the Ground Up</h2>
 <p>Need more room without moving? We frame, roof, side and finish room additions, primary suites and garage additions so they match your existing home. Roofing is our core trade — so the tie-in between the old roof and the new one, where most additions leak, is done right.</p>
 <a class="btn btn-green" href="/home-additions/">Home Addition Services</a></div>
 <div><img class="tall" src="{img("addition_wrap",1000)}" alt="Home addition under construction with house wrap" loading="lazy"></div></div>
 <div class="wrap"><figure class="wide-photo"><img src="{img("framing",1600)}" alt="Room addition framing by C.E. Enterprises in Indianapolis" loading="lazy"><figcaption>A C.E. Enterprises room addition in the framing stage.</figcaption></figure></div></section>
<section class="sec alt" id="work"><div class="wrap"><p class="eyebrow">Real projects</p><h2>Our Work</h2><p class="center sub">Every photo here is a C.E. Enterprises job, straight from our Google Business Profile.</p><div class="gallery">{gal}</div></div></section>
{reviews_html()}
<section class="sec" id="areas"><div class="wrap"><p class="eyebrow">Service areas</p><h2>Serving the Indianapolis Metro — 40-Mile Radius</h2><div class="areas">{areas}</div>
<div class="map"><iframe title="C.E. Enterprises location" loading="lazy" src="https://www.google.com/maps?q=2065+S+Kitley+Ave,+Indianapolis,+IN+46203&output=embed"></iframe></div></div></section>
<section class="sec alt"><div class="wrap two"><div><p class="eyebrow">How it works</p><h2>Booking an Estimate</h2>
<ol class="steps"><li><b>Call or send the form.</b> Tell us what's going on — leak, storm damage, new siding, an addition or a remodel.</li><li><b>On-site visit.</b> Chris comes out, inspects, takes photos and listens to what you want.</li><li><b>Written estimate.</b> Clear scope and price, no pressure.</li><li><b>We build it.</b> One crew, clean site, regular updates through the final walkthrough.</li></ol></div>
<div id="quote" class="qwrap">{quote_form("Request Your Free Estimate")}</div></div></section>
{faq}'''
    page("/", "Roofing Contractor Indianapolis IN | Siding, Additions & Remodeling | C.E. Enterprises",
         "Owner-operated roofing, siding, home additions, custom homes, kitchen & bath remodeling in Indianapolis, Greenwood, Westfield, Noblesville & Avon. Call (317) 402-9681.",
         body, [fsch])

SUBLINK = {"Roof Inspection":"roof-inspection","Roof Repair":"roof-repair","Roof Replacement & Re-Roofing":"roof-replacement",
 "Storm Damage & Emergency Roofing":"storm-damage-roof-repair","Shingle Roofs":"shingle-roofing","Metal Roofs":"metal-roofing",
 "Rubber (EPDM) & Flat Roofs":"rubber-roofing","Tile & Specialty Roofs":"tile-roofing"}
def sub_card(t, d, label=None):
    label = label or t
    if t in SUBLINK:
        return f'<a class="sub sublink" href="/{SUBLINK[t]}/"><h3>{e(label)}</h3><p>{e(d)}</p><span>Learn more →</span></a>'
    return f'<div class="sub"><h3>{e(label)}</h3><p>{e(d)}</p></div>'

def build_service(s):
    subs = "".join(sub_card(t,d) for t,d in s["subs"])
    links = " · ".join(f'<a href="/roofing-contractor-{c["slug"]}-in/">{c["name"]}</a>' for c in CITIES)
    extra = ""
    if s["slug"] == "home-additions":
        extra = f'<figure class="wide-photo"><img src="{img("framing",1600)}" alt="Room addition framing in Indianapolis" loading="lazy"><figcaption>Room addition framing by C.E. Enterprises.</figcaption></figure>'
    pics = {"roofing":["roof_cedar","roof_slate","exterior_patio"],"siding":["new_build","addition_wrap","exterior_patio"],
            "home-additions":["addition_wrap","framing","new_build"],"custom-home-builder":["new_build","framing","kitchen2"],
            "kitchen-remodeling":["kitchen1","kitchen2","showroom"],"bathroom-remodeling":["shower_glass","tub_free","bath_wood","bath_lit","bath_marble","bath_white"],
            "full-home-renovation":["showroom","reno_progress","kitchen2"]}[s["slug"]]
    gal = "".join(f'<img src="{img(k,700)}" alt="{e(s["nav"])} project by C.E. Enterprises" loading="lazy">' for k in pics)
    faqs = [(f"Do you offer {s['nav'].lower()} for commercial properties?","Yes. We work on both residential and commercial properties across the Indianapolis metro."),
            (f"Where do you offer {s['nav'].lower()}?","Indianapolis, Greenwood, Westfield, Noblesville, Avon and communities within about 40 miles of our Indianapolis shop."),
            ("How do I get a price?",f"Call {BIZ['phone']} or use the estimate form. Estimates are free.")]
    faq, fsch = faq_html(faqs)
    svc_schema = {"@context":"https://schema.org","@type":"Service","serviceType":s["nav"],"provider":{"@type":"LocalBusiness","name":BIZ["name"],"telephone":BIZ["tel"]},"areaServed":[f'{c["name"]}, IN' for c in CITIES]}
    body = f'''
<section class="phero" style="--bg:url('{img(s["photo"],1800)}')"><div class="wrap"><p class="crumb"><a href="/">Home</a> / {s["nav"]}</p><h1>{s["h1"]}</h1><p class="lead">{e(s["intro"])}</p>
<div class="hero-cta"><a class="btn btn-gold btn-lg" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a><a class="btn btn-ghost btn-lg" href="#quote">Free Estimate</a></div></div></section>
<section class="sec"><div class="wrap"><h2>{s["nav"]} Services</h2><div class="subs">{subs}</div>{extra}</div></section>
<section class="sec alt"><div class="wrap"><h2>Recent {s["nav"]} Work</h2><div class="gallery">{gal}</div></div></section>
{reviews_html()}
<section class="sec"><div class="wrap two"><div><h2>{s["nav"]} Near You</h2><p>We provide {s["nav"].lower()} for homes and businesses in {links} and the surrounding area — about a 40-mile radius from our shop at {BIZ["street"]}, Indianapolis.</p>
<ul class="checks"><li>Owner Chris Epple on every project</li><li>BBB Accredited since 2019</li><li>Residential &amp; commercial</li><li>Free estimates</li></ul></div><div id="quote">{quote_form()}</div></div></section>
{faq}'''
    page(f'/{s["slug"]}/', s["title"], s["desc"], body, [svc_schema, fsch], imgabs(s["photo"]))

def build_kw(p):
    secs = "".join(f'<div class="kwsec"><h2>{e(h)}</h2>{b if b.lstrip().startswith("<") else "<p>"+b+"</p>"}</div>' for h,b in p["sections"])
    rc = ""
    if p["res"] or p["com"]:
        rc = f'''<section class="sec alt"><div class="wrap"><h2>Residential &amp; Commercial {e(p["nav"])}</h2><div class="subs two-up">
<div class="sub"><h3>Residential</h3><p>{e(p["res"])}</p></div><div class="sub"><h3>Commercial</h3><p>{e(p["com"])}</p></div></div></div></section>'''
    links = " · ".join(f'<a href="/roofing-contractor-{c["slug"]}-in/">{c["name"]}</a>' for c in CITIES)
    related = "".join(f'<li><a href="/{q["slug"]}/">{q["nav"]}</a></li>' for q in PAGES if q["slug"]!=p["slug"])
    faq, fsch = faq_html(p["faqs"])
    svc_schema = {"@context":"https://schema.org","@type":"Service","serviceType":p["nav"],"name":p["h1"],
                  "provider":{"@type":"RoofingContractor","name":BIZ["name"],"telephone":BIZ["tel"],"address":{"@type":"PostalAddress","streetAddress":BIZ["street"],"addressLocality":BIZ["city"],"addressRegion":BIZ["state"],"postalCode":BIZ["zip"]}},
                  "areaServed":[f'{c["name"]}, IN' for c in CITIES]}
    crumb = {"@context":"https://schema.org","@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Home","item":DOMAIN+"/"},{"@type":"ListItem","position":2,"name":p["nav"],"item":f'{DOMAIN}/{p["slug"]}/'}]}
    body = f'''
<section class="phero" style="--bg:url('{img(p["photo"],1800)}')"><div class="wrap"><p class="crumb"><a href="/">Home</a> / {p["nav"]}</p><h1>{e(p["h1"])}</h1><p class="lead">{e(p["intro"])}</p>
<div class="hero-cta"><a class="btn btn-gold btn-lg" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a><a class="btn btn-ghost btn-lg" href="#quote">Free Estimate</a></div>
<ul class="trust"><li>★ 4.8 Google rating</li><li>BBB Accredited since 2019</li><li>Residential &amp; Commercial</li></ul></div></section>
<section class="sec"><div class="wrap kwgrid">{secs}</div></section>
{rc}
{reviews_html()}
<section class="sec"><div class="wrap two"><div><h2>{e(p["nav"])} Near You</h2><p>C.E. Enterprises provides {e(p["nav"].lower())} in {links} and the surrounding area — about a 40-mile radius from our shop at {BIZ["street"]}, Indianapolis.</p>
<h3>Related services</h3><ul class="links">{related}</ul></div><div id="quote">{quote_form(f"Free {p['nav']} Estimate")}</div></div></section>
{faq}'''
    page(f'/{p["slug"]}/', p["title"], p["desc"], body, [svc_schema, crumb, fsch], imgabs(p["photo"]))

def build_city(c):
    roof = SERVICES[0]
    subs = "".join(sub_card(t, d, f"{t} in {c['name']}") for t,d in roof["subs"])
    other = "".join(f'<li><a href="/{s["slug"]}/">{s["nav"]} in {c["name"]}</a></li>' for s in SERVICES[1:])
    faqs = [(f"Do you offer roof repair in {c['name']}, IN?",f"Yes. We handle roof repairs, replacements, inspections and storm damage in {c['name']} for homes and commercial buildings. Call {BIZ['phone']}."),
            (f"Do you install siding in {c['name']}?","Yes — siding installation, replacement and repair, often paired with roofing so the whole exterior is done at once."),
            (f"Do you build home additions in {c['name']}?","Yes. We build room additions, primary suites and garage additions, including the roofing and siding tie-in.")]
    faq, fsch = faq_html(faqs)
    body = f'''
<section class="phero" style="--bg:url('{img("roof_slate",1800)}')"><div class="wrap"><p class="crumb"><a href="/">Home</a> / Service Areas / {c["name"]}</p>
<h1>Roofing &amp; Siding Contractor in {c["name"]}, IN</h1><p class="lead">Roof repair, roof replacement, siding, home additions and remodeling for {c["name"]} homes and businesses. {e(c["note"])}</p>
<div class="hero-cta"><a class="btn btn-gold btn-lg" href="tel:{BIZ["tel"]}">Call {BIZ["phone"]}</a><a class="btn btn-ghost btn-lg" href="#quote">Free Estimate</a></div></div></section>
<section class="sec"><div class="wrap"><h2>Roofing Services in {c["name"]}</h2><div class="subs">{subs}</div>
<p>Need more than a roof? We also handle:</p><ul class="links">{other}<li><a href="/commercial-roofing/">Commercial roofing in {c["name"]}</a></li><li><a href="/general-contractor/">General contractor in {c["name"]}</a></li></ul></div></section>
{reviews_html()}
<section class="sec alt"><div class="wrap two"><div><h2>Why {c["name"]} Homeowners Call C.E. Enterprises</h2>
<ul class="checks"><li>Owner-operated — you work directly with Chris Epple</li><li>BBB Accredited since 2019</li><li>4.8★ Google rating</li><li>Roofing, siding and remodeling under one contractor</li><li>Residential &amp; commercial</li></ul>
<img src="{img("exterior_patio",900)}" alt="Home exterior by C.E. Enterprises" loading="lazy" class="rounded"></div><div id="quote">{quote_form(f"Free Estimate in {c['name']}")}</div></div></section>
{faq}'''
    page(f'/roofing-contractor-{c["slug"]}-in/', f'Roofing Contractor {c["name"]} IN | Roof Repair, Siding & Additions | C.E. Enterprises',
         f'Roof repair, roof replacement, siding and home additions in {c["name"]}, IN. Residential & commercial. Owner-operated, BBB accredited. Call (317) 402-9681.', body, [fsch])

def build_blog():
    posts = POSTS + [json.load(open(f)) for f in sorted(glob.glob("posts/*.json"))]
    posts.sort(key=lambda p: p["date"], reverse=True)
    for p in posts:
        art = {"@context":"https://schema.org","@type":"BlogPosting","headline":p["title"],"description":p["desc"],"datePublished":p["date"],"image":imgabs(p["photo"]),
               "author":{"@type":"Person","name":BIZ["owner"]},"publisher":{"@type":"Organization","name":BIZ["name"],"logo":{"@type":"ImageObject","url":DOMAIN+"/img/logo.png"}},
               "mainEntityOfPage":f'{DOMAIN}/blog/{p["slug"]}/'}
        body = f'''<section class="phero short" style="--bg:url('{img(p["photo"],1800)}')"><div class="wrap narrow"><p class="crumb"><a href="/">Home</a> / <a href="/blog/">Blog</a></p><h1>{e(p["title"])}</h1>
<p class="meta">By {BIZ["owner"]} · {datetime.date.fromisoformat(p["date"]).strftime("%B %d, %Y")}</p></div></section>
<article class="sec"><div class="wrap narrow post">{p["body"]}</div></article>
<section class="sec alt"><div class="wrap narrow">{quote_form("Free Roof Inspection & Estimate")}</div></section>'''
        page(f'/blog/{p["slug"]}/', p["title"] + " | C.E. Enterprises", p["desc"], body, [art], imgabs(p["photo"]))
    cards = "".join(f'<a class="card" href="/blog/{p["slug"]}/"><img src="{img(p["photo"],800)}" alt="" loading="lazy"><div><h3>{e(p["title"])}</h3><p>{e(p["desc"])}</p><span>Read more →</span></div></a>' for p in posts)
    page("/blog/", "Roofing, Siding & Remodeling Blog | C.E. Enterprises Indianapolis",
         "Roofing, siding, home addition and remodeling advice for Indianapolis-area homeowners from C.E. Enterprises.",
         f'<section class="phero short" style="--bg:url(\'{img("roof_cedar",1800)}\')"><div class="wrap"><h1>Roofing &amp; Remodeling Blog</h1><p class="lead">Straight answers for Indianapolis-area homeowners.</p></div></section><section class="sec"><div class="wrap"><div class="cards">{cards}</div></div></section>')
    # RSS feed (for Blotato / social pipeline)
    items = "".join(f'''<item><title>{e(p["title"])}</title><link>{DOMAIN}/blog/{p["slug"]}/</link><guid>{DOMAIN}/blog/{p["slug"]}/</guid>
<pubDate>{datetime.datetime.fromisoformat(p["date"]+"T09:00:00-04:00").strftime("%a, %d %b %Y %H:%M:%S %z")}</pubDate><description>{e(p["desc"])}</description>
<enclosure url="{e(imgabs(p["photo"]))}" type="image/jpeg" length="0"/></item>''' for p in posts)
    open("public/feed.xml","w").write(f'<?xml version="1.0" encoding="UTF-8"?><rss version="2.0"><channel><title>C.E. Enterprises Blog</title><link>{DOMAIN}/blog/</link><description>Roofing, siding and remodeling advice for the Indianapolis area.</description><language>en-us</language>{items}</channel></rss>')
    return posts

def main():
    if os.path.exists("public"): shutil.rmtree("public")
    os.makedirs("public/img"); open("public/img/logo.png","wb").write(__import__("base64").b64decode(LOGO_B64)); shutil.copy("style.css","public/style.css")
    build_home()
    for s in SERVICES: build_service(s)
    for c in CITIES: build_city(c)
    for p in PAGES: build_kw(p)
    posts = build_blog()
    urls = ["/"]+[f'/{s["slug"]}/' for s in SERVICES]+[f'/{p["slug"]}/' for p in PAGES]+[f'/roofing-contractor-{c["slug"]}-in/' for c in CITIES]+["/blog/"]+[f'/blog/{p["slug"]}/' for p in posts]
    today = datetime.date.today().isoformat()
    open("public/sitemap.xml","w").write('<?xml version="1.0" encoding="UTF-8"?><urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'+"".join(f"<url><loc>{DOMAIN}{u}</loc><lastmod>{today}</lastmod></url>" for u in urls)+"</urlset>")
    open("public/robots.txt","w").write(f"User-agent: *\nAllow: /\nSitemap: {DOMAIN}/sitemap.xml\n")
    rw=[{"source":f"/p/{k}-:w(\\d+).jpg","destination":f"{G}{v}=w:w"} for k,v in P.items()]
    json.dump({"trailingSlash":True,"rewrites":rw,"headers":[{"source":"/p/(.*)","headers":[{"key":"Cache-Control","value":"public, max-age=604800"}]}]},open("public/vercel.json","w"),indent=0)
    print(len(urls), "pages built")

if __name__ == "__main__": main()
