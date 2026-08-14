import adsk.core, adsk.fusion, traceback


def draw_capsule(sketch, total_len, total_w):
    lines = sketch.sketchCurves.sketchLines
    arcs = sketch.sketchCurves.sketchArcs

    r = total_w / 2.0
    x1 = -total_len / 2.0 + r
    x2 = total_len / 2.0 - r
    x_far_left = -total_len / 2.0
    x_far_right = total_len / 2.0

    top_left = adsk.core.Point3D.create(x1, r, 0)
    top_right = adsk.core.Point3D.create(x2, r, 0)
    bottom_left = adsk.core.Point3D.create(x1, -r, 0)
    bottom_right = adsk.core.Point3D.create(x2, -r, 0)

    left_mid = adsk.core.Point3D.create(x_far_left, 0, 0)
    right_mid = adsk.core.Point3D.create(x_far_right, 0, 0)

    lines.addByTwoPoints(top_left, top_right)
    lines.addByTwoPoints(bottom_right, bottom_left)

    arcs.addByThreePoints(bottom_left, left_mid, top_left)
    arcs.addByThreePoints(top_right, right_mid, bottom_right)


def biggest_profile(sketch):
    best = None
    best_area = -1

    for i in range(sketch.profiles.count):
        p = sketch.profiles.item(i)
        bb = p.boundingBox
        area = (bb.maxPoint.x - bb.minPoint.x) * (bb.maxPoint.y - bb.minPoint.y)
        if area > best_area:
            best_area = area
            best = p

    return best


def run(context):
    ui = None
    try:
        app = adsk.core.Application.get()
        ui = app.userInterface
        design = adsk.fusion.Design.cast(app.activeProduct)

        if not design:
            ui.messageBox('Nema aktivnog Fusion 360 dizajna.')
            return

        root = design.rootComponent
        sketches = root.sketches
        extrudes = root.features.extrudeFeatures
        planes = root.constructionPlanes

        mm = 0.1  # Fusion createByReal koristi cm

        # PARAMETRI
        outer_len = 95 * mm
        outer_w = 38 * mm
        outer_h = 12 * mm

        cavity_len = 82 * mm
        cavity_w = 24 * mm
        cavity_d = 4.5 * mm

        dot_d = 2.4 * mm
        dot_h = 0.8 * mm
        pitch_x = 7 * mm   # razmak po dužini
        pitch_y = 6 * mm   # razmak po širini

        xy = root.xYConstructionPlane

        # 1. Vanjski oblik
        sk_outer = sketches.add(xy)
        draw_capsule(sk_outer, outer_len, outer_w)

        outer_prof = biggest_profile(sk_outer)
        if not outer_prof:
            ui.messageBox('Greška: vanjski profil nije napravljen.')
            return

        outer_input = extrudes.createInput(
            outer_prof,
            adsk.fusion.FeatureOperations.NewBodyFeatureOperation
        )
        outer_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(outer_h))
        outer_ext = extrudes.add(outer_input)
        mold_body = outer_ext.bodies.item(0)
        mold_body.name = 'HurmasicaKalup'

        # 2. Offset ravan na vrhu
        top_plane_input = planes.createInput()
        top_plane_input.setByOffset(
            xy,
            adsk.core.ValueInput.createByReal(outer_h)
        )
        top_plane = planes.add(top_plane_input)

        # 3. Unutrašnji kanal
        sk_cavity = sketches.add(top_plane)
        draw_capsule(sk_cavity, cavity_len, cavity_w)

        cavity_prof = biggest_profile(sk_cavity)
        if not cavity_prof:
            ui.messageBox('Greška: cavity profil nije napravljen.')
            return

        cavity_input = extrudes.createInput(
            cavity_prof,
            adsk.fusion.FeatureOperations.CutFeatureOperation
        )
        cavity_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(cavity_d))
        cavity_input.participantBodies = [mold_body]
        extrudes.add(cavity_input)

        # 4. Offset ravan na dnu cavity-ja
        bottom_plane_input = planes.createInput()
        bottom_plane_input.setByOffset(
            xy,
            adsk.core.ValueInput.createByReal(outer_h - cavity_d)
        )
        bottom_plane = planes.add(bottom_plane_input)

        # 5. Tačkice
        sk_dots = sketches.add(bottom_plane)
        circles = sk_dots.sketchCurves.sketchCircles

        r = cavity_w / 2.0
        x1 = -cavity_len / 2.0 + r
        x2 = cavity_len / 2.0 - r
        x_far_left = -cavity_len / 2.0
        x_far_right = cavity_len / 2.0

        margin = dot_d / 2.0 + 0.4 * mm

        x = x1 + margin
        dot_count = 0
        while x <= x2 - margin + 1e-9:
            y = -r + margin
            while y <= r - margin + 1e-9:
                inside = False

                if x >= x1 and x <= x2:
                    inside = abs(y) <= (r - margin)
                elif x < x1:
                    inside = ((x - x1) ** 2 + y ** 2) <= (r - margin) ** 2
                elif x > x2:
                    inside = ((x - x2) ** 2 + y ** 2) <= (r - margin) ** 2

                if inside:
                    circles.addByCenterRadius(
                        adsk.core.Point3D.create(x, y, 0),
                        dot_d / 2.0
                    )
                    dot_count += 1

                y += pitch_y
            x += pitch_x

        if sk_dots.profiles.count == 0:
            ui.messageBox('Greška: tačkice nisu generisane.')
            return

        for i in range(sk_dots.profiles.count):
            prof = sk_dots.profiles.item(i)
            dot_input = extrudes.createInput(
                prof,
                adsk.fusion.FeatureOperations.JoinFeatureOperation
            )
            dot_input.setDistanceExtent(False, adsk.core.ValueInput.createByReal(dot_h))
            dot_input.participantBodies = [mold_body]
            extrudes.add(dot_input)

        ui.messageBox(
            'Kalup je uspješno napravljen.\\n\\n'
            'Vanjski: 95 x 38 x 12 mm\\n'
            'Kanal: 82 x 24 x 4.5 mm\\n'
            'Tačkice: Ø2.4 mm, visina 0.8 mm\\n'
            'Broj tačkica: {}'.format(dot_count)
        )

    except:
        if ui:
            ui.messageBox('Failed:\\n{}'.format(traceback.format_exc()))