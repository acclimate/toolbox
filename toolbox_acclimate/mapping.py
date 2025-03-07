#!/usr/bin/python3 -W ignore

import gzip
import math
import pickle

import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PatchCollection
from matplotlib.colors import LinearSegmentedColormap, Normalize
from matplotlib.patches import PathPatch, Wedge
from pyproj import Transformer
from shapely.ops import transform
from shapely.geometry import Point
from shapely import affinity

from toolbox_acclimate.definitions import region_names


def create_colormap(name, colors, alphas=None, xs=None):
    def get_rgb1(c, alpha=1):
        return tuple(list(matplotlib.colors.hex2color(c)) + [alpha])

    if str(matplotlib.__version__).startswith("2"):
        get_rgb = matplotlib.colors.to_rgba
    else:
        get_rgb = get_rgb1
    if alphas is None:
        colors = [get_rgb(c) for c in colors]
    else:
        colors = [get_rgb(c, alpha=a) for c, a in zip(colors, alphas)]
    if xs is None:
        xs = np.linspace(0, 1, len(colors))
    res = LinearSegmentedColormap(
        name,
        {
            channel: tuple(
                (x, float(c[channel_id]), float(c[channel_id]))
                for c, x in zip(colors, xs)
            )
            for channel_id, channel in enumerate(["red", "green", "blue", "alpha"])
        },
        N=2048,
    )
    res.set_under(colors[0])
    res.set_over(colors[-1])
    return res


def make_map(
        patchespickle_file,
        map_regions=None,
        map_data=None,
        show_cbar=True,
        centroids_regions=None,
        centroids_data=None,
        centroids_data_unit=None,
        centroids_annotate=None,
        centroids_alpha=.7,
        centroids_max_size=.05,
        centroids_legend=True,
        cm=None,
        symmetric_cmap=False,
        center_zero=False,
        outfile=None,
        extend_c='both',
        numbering=None,
        y_label=None,
        rasterize=True,
        min_lon=-156,
        max_lon=170,
        min_lat=-58,
        max_lat=89,
        valid_ec='black',
        inv_fc='lightgrey',
        inv_ec='black',
        inv_hatch=False,
        map_v_limits=None,
        centroids_v_limits=None,
        figsize=None,
        ax=None,
        cax=None,
        cbar_orientation='vertical',
        exclude_regions=None,
        silently_exclude_regions=None,
):
    if map_data is None and centroids_data is None:
        raise ValueError("Must pass at least one of map_data and centroids_data to plot.")

    if centroids_annotate is None:
        centroids_annotate = []

    if exclude_regions is None:
        exclude_regions = []

    if silently_exclude_regions is None:
        silently_exclude_regions = []

    patchespickle = pickle.load(gzip.GzipFile(patchespickle_file, "rb"))
    patches = patchespickle["patches"]
    projection_name = patchespickle["projection"]

    if cm is None:
        cm = create_colormap("custom", ["red", "white", "blue"], xs=[0, 0.5, 1])

    projection = Transformer.from_crs("EPSG:4326", projection_name)

    minx = transform(projection.transform, Point(0, min_lon)).x
    maxx = transform(projection.transform, Point(0, max_lon)).x
    miny = transform(projection.transform, Point(min_lat, 0)).y
    maxy = transform(projection.transform, Point(max_lat, 0)).y

    if ax == cax == None:
        fig, (ax, cax) = plt.subplots(
            ncols=2,
            gridspec_kw={'width_ratios': [.975, .025]},
            figsize=(7.07, 3.3) if figsize is None else figsize
        )

    ax.set_aspect(1)
    ax.axis("off")

    ax.set_xlim((minx, maxx))
    ax.set_ylim((miny, maxy))

    validpatches = {}
    validpatches_data = {}
    invpatches = {}
    silentpatches = {}
    if map_data is not None:
        if map_v_limits is None:
            map_vmin = np.min(map_data)
            map_vmax = np.max(map_data)
        else:
            (map_vmin, map_vmax) = map_v_limits
        if symmetric_cmap and np.sign(map_vmin) != np.sign(map_vmax):
            v = max(abs(map_vmin), abs(map_vmax))
            (map_vmin, map_vmax) = (np.sign(map_vmin) * v, np.sign(map_vmax) * v)
        if center_zero:
            v = max(abs(map_vmin), abs(map_vmax))
            (map_vmin, map_vmax) = (-v,v)

        norm_color = Normalize(vmin=map_vmin, vmax=map_vmax)
        for r, d in zip(map_regions, map_data):
            if r in patches:
                level, subregions, patch = patches[r]
                if math.isnan(d):
                    invpatches[r] = patch
                    print(f'NAN data for region {r}')
                elif r in exclude_regions:
                    invpatches[r] = patch
                    print(f'excluding region {r}')
                else:
                    validpatches[r] = patch
                    validpatches_data[r] = d
            else:
                print(f"Region {r} not found in patches.")
        valid_collection = ax.add_collection(
            PatchCollection(
                list(validpatches.values()),
                edgecolors=valid_ec,
                facecolors="black",
                linewidths=.1,
                rasterized=rasterize,
                zorder=1
            )
        )
        valid_collection.set_facecolors(cm(norm_color([validpatches_data[k] for k in validpatches.keys()])))
        if cax is not None:
            cbar = matplotlib.colorbar.ColorbarBase(
                cax,
                cmap=cm,
                norm=norm_color,
                orientation=cbar_orientation,
                spacing="proportional",
                extend=extend_c,
            )
            cbar.minorticks_on()
            cax.set_ylabel(y_label)

    for r, (level, subregions, patch) in patches.items():
        # if len(subregions) == 1 and r not in validpatches and r not in invpatches:
        if r not in validpatches and r not in invpatches:
            if r in region_names and r not in silently_exclude_regions:
                invpatches[r] = patch
                print('No data passed for region {}'.format(r))
            elif r in exclude_regions and r not in silently_exclude_regions:
                invpatches[r] = patch
                print(f'excluding region {r}')
            elif level == 0:
                silentpatches[r] = patch

    ax.add_collection(
        PatchCollection(
            list(invpatches.values()),
            hatch="///" if inv_hatch else None,
            facecolors=inv_fc,
            edgecolors=inv_ec,
            linewidths=.1,
            rasterized=rasterize,
            zorder=0
        )
    )

    ax.add_collection(
        PatchCollection(
            list(silentpatches.values()),
            facecolors='none',
            edgecolors=valid_ec,
            linewidths=.1,
            rasterized=rasterize,
            zorder=0
        )
    )

    if centroids_data is not None:
        centroids = patchespickle["centroids"]
        if centroids_v_limits is None:
            centroids_vmin = np.min(centroids_data)
            centroids_vmax = np.max(centroids_data)
        else:
            (centroids_vmin, centroids_vmax) = centroids_v_limits

        def get_radius(_d):
            return centroids_max_size * np.sqrt(_d) / np.sqrt(centroids_vmax) * (abs(ax.get_ylim()[0]) + abs(ax.get_ylim()[1]))
        wedges = []
        for r, d in zip(centroids_regions, centroids_data):
            if r in centroids:
                wedges.append(Wedge(centroids[r], get_radius(d), 0, 360))
                if r in centroids_annotate:
                    ax.text(centroids[r].x, centroids[r].y, r, ha='center', va='center')
        legend_wedges = []
        x_pos = ax.get_xlim()[0] + get_radius(centroids_vmin)
        y_pos = ax.get_ylim()[0] + get_radius(centroids_vmax)
        ax.add_collection(
            PatchCollection(
                wedges,
                facecolors='lightgrey',
                edgecolors='grey',
                linewidths=.1,
                rasterized=rasterize,
                zorder=1,
                alpha=centroids_alpha
            )
        )
        if centroids_legend:
            for d in np.linspace(centroids_vmin, centroids_vmax, 3):
                radius = get_radius(d)
                # x_pos += 2 * radius
                x_pos += .05 * (abs(ax.get_xlim()[0]) + abs(ax.get_xlim()[1]))
                legend_wedges.append(Wedge((x_pos, y_pos), radius, 0, 360))
                text = f"{int(np.round(d, 0))}"
                if centroids_data_unit is not None:
                    text += "{}".format(centroids_data_unit)
                ax.text(x_pos + radius * 1.1, y_pos, text, ha='center', va='center')
            ax.add_collection(
                PatchCollection(
                    legend_wedges,
                    facecolors='lightgrey',
                    edgecolors='grey',
                    linewidths=.1,
                    rasterized=rasterize,
                    zorder=1,
                )
            )

    plt.tight_layout()

    if not show_cbar and cax is not None:
        cax.set_visible(False)

    if numbering is not None:
        tran = matplotlib.transforms.blended_transform_factory(fig.transFigure, ax.transAxes)
        ax.text(0.0, 1.0, numbering, transform=tran, fontweight='bold', ha='left', va='top')

    if outfile is not None:
        fig.savefig(outfile, dpi=300)
