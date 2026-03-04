# analysis.py
from qgis.core import (
    QgsField, QgsSpatialIndex, QgsVectorDataProvider,
    QgsProject, QgsVectorLayer
)
from PyQt5.QtCore import QVariant
from PyQt5.QtWidgets import QMessageBox

def compare_layers(layer_list, thresh=0.8, progress_callback=None):
    base: QgsVectorLayer = layer_list[0]

    # 0. 检查
    if not (base.dataProvider().capabilities() &
            QgsVectorDataProvider.AddAttributes):
        QMessageBox.warning(None, "Read Only",
                            "Unable to build field，Please save as Shapefile or GeoPackage")
        return base

    base.startEditing()

    # 1. 字段
    def ensure_field(name, vtype):
        idx = base.fields().indexFromName(name)
        if idx == -1:
            base.dataProvider().addAttributes([QgsField(name, vtype)])
            base.updateFields()
            idx = base.fields().indexFromName(name)
        return idx

    pc_idx = ensure_field("persistence_count", QVariant.Int)
    pr_idx = ensure_field("persistence_ratio", QVariant.Double)
    ip_idx = ensure_field("is_persistent", QVariant.Bool)

    # 2. 字段清零
    for f in base.getFeatures():
        base.changeAttributeValue(f.id(), pc_idx, 1)
        base.changeAttributeValue(f.id(), pr_idx, 1.0)
        base.changeAttributeValue(f.id(), ip_idx, False)

    # 3. 索引
    sidx = QgsSpatialIndex(base.getFeatures())
    total = sum(l.featureCount() for l in layer_list[1:])
    done = 0

    for other in layer_list[1:]:
        for ofeat in other.getFeatures():
            cand = sidx.intersects(ofeat.geometry().boundingBox())
            for bid in cand:
                bfeat = base.getFeature(bid)
                inter = bfeat.geometry().intersection(ofeat.geometry())
                if inter.isEmpty():
                    continue
                ratio = inter.area() / bfeat.geometry().area()
                if ratio >= thresh:
                    cur_cnt = bfeat.attribute(pc_idx)
                    cur_rat = bfeat.attribute(pr_idx)
                    base.changeAttributeValue(bid, pc_idx, cur_cnt + 1)
                    base.changeAttributeValue(bid, pr_idx,
                                              max(cur_rat, round(ratio, 2)))
            done += 1
            if progress_callback:
                progress_callback(int(done / total * 100))

    # 4. 标记持续存在
    periods = len(layer_list)
    for f in base.getFeatures():
        flag = (f.attribute(pc_idx) == periods)
        base.changeAttributeValue(f.id(), ip_idx, flag)

    base.commitChanges()
    base.triggerRepaint()
    if progress_callback:
        progress_callback(100)
    return base
