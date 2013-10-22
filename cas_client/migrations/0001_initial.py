# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Department'
        db.create_table('cas_client_department', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
        ))
        db.send_create_signal('cas_client', ['Department'])

        # Adding model 'Subject'
        db.create_table('cas_client_subject', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('number', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=1200, null=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('term', self.gf('django.db.models.fields.CharField')(max_length=1, null=True, blank=True)),
            ('year', self.gf('django.db.models.fields.CharField')(max_length=4, null=True, blank=True)),
        ))
        db.send_create_signal('cas_client', ['Subject'])

        # Adding M2M table for field prerequisites on 'Subject'
        db.create_table('cas_client_subject_prerequisites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_subject', models.ForeignKey(orm['cas_client.subject'], null=False)),
            ('to_subject', models.ForeignKey(orm['cas_client.subject'], null=False))
        ))
        db.create_unique('cas_client_subject_prerequisites', ['from_subject_id', 'to_subject_id'])

        # Adding model 'Keyword'
        db.create_table('cas_client_keyword', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('cas_client', ['Keyword'])

        # Adding model 'Module'
        db.create_table('cas_client_module', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=60)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=600, null=True, blank=True)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(related_name='creator', to=orm['auth.User'])),
        ))
        db.send_create_signal('cas_client', ['Module'])

        # Adding M2M table for field subjects on 'Module'
        db.create_table('cas_client_module_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('module', models.ForeignKey(orm['cas_client.module'], null=False)),
            ('subject', models.ForeignKey(orm['cas_client.subject'], null=False))
        ))
        db.create_unique('cas_client_module_subjects', ['module_id', 'subject_id'])

        # Adding model 'Outcome'
        db.create_table('cas_client_outcome', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('description', self.gf('django.db.models.fields.CharField')(max_length=400)),
            ('creator', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
        ))
        db.send_create_signal('cas_client', ['Outcome'])

        # Adding M2M table for field prerequisites on 'Outcome'
        db.create_table('cas_client_outcome_prerequisites', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('from_outcome', models.ForeignKey(orm['cas_client.outcome'], null=False)),
            ('to_outcome', models.ForeignKey(orm['cas_client.outcome'], null=False))
        ))
        db.create_unique('cas_client_outcome_prerequisites', ['from_outcome_id', 'to_outcome_id'])

        # Adding M2M table for field modules on 'Outcome'
        db.create_table('cas_client_outcome_modules', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('outcome', models.ForeignKey(orm['cas_client.outcome'], null=False)),
            ('module', models.ForeignKey(orm['cas_client.module'], null=False))
        ))
        db.create_unique('cas_client_outcome_modules', ['outcome_id', 'module_id'])

        # Adding M2M table for field subjects on 'Outcome'
        db.create_table('cas_client_outcome_subjects', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('outcome', models.ForeignKey(orm['cas_client.outcome'], null=False)),
            ('subject', models.ForeignKey(orm['cas_client.subject'], null=False))
        ))
        db.create_unique('cas_client_outcome_subjects', ['outcome_id', 'subject_id'])

        # Adding M2M table for field departments on 'Outcome'
        db.create_table('cas_client_outcome_departments', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('outcome', models.ForeignKey(orm['cas_client.outcome'], null=False)),
            ('department', models.ForeignKey(orm['cas_client.department'], null=False))
        ))
        db.create_unique('cas_client_outcome_departments', ['outcome_id', 'department_id'])

        # Adding M2M table for field keywords on 'Outcome'
        db.create_table('cas_client_outcome_keywords', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('outcome', models.ForeignKey(orm['cas_client.outcome'], null=False)),
            ('keyword', models.ForeignKey(orm['cas_client.keyword'], null=False))
        ))
        db.create_unique('cas_client_outcome_keywords', ['outcome_id', 'keyword_id'])


    def backwards(self, orm):
        # Deleting model 'Department'
        db.delete_table('cas_client_department')

        # Deleting model 'Subject'
        db.delete_table('cas_client_subject')

        # Removing M2M table for field prerequisites on 'Subject'
        db.delete_table('cas_client_subject_prerequisites')

        # Deleting model 'Keyword'
        db.delete_table('cas_client_keyword')

        # Deleting model 'Module'
        db.delete_table('cas_client_module')

        # Removing M2M table for field subjects on 'Module'
        db.delete_table('cas_client_module_subjects')

        # Deleting model 'Outcome'
        db.delete_table('cas_client_outcome')

        # Removing M2M table for field prerequisites on 'Outcome'
        db.delete_table('cas_client_outcome_prerequisites')

        # Removing M2M table for field modules on 'Outcome'
        db.delete_table('cas_client_outcome_modules')

        # Removing M2M table for field subjects on 'Outcome'
        db.delete_table('cas_client_outcome_subjects')

        # Removing M2M table for field departments on 'Outcome'
        db.delete_table('cas_client_outcome_departments')

        # Removing M2M table for field keywords on 'Outcome'
        db.delete_table('cas_client_outcome_keywords')


    models = {
        'auth.group': {
            'Meta': {'object_name': 'Group'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        'auth.permission': {
            'Meta': {'ordering': "('content_type__app_label', 'content_type__model', 'codename')", 'unique_together': "(('content_type', 'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['contenttypes.ContentType']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        'cas_client.department': {
            'Meta': {'object_name': 'Department'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'})
        },
        'cas_client.keyword': {
            'Meta': {'ordering': "['name']", 'object_name': 'Keyword'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'})
        },
        'cas_client.module': {
            'Meta': {'object_name': 'Module'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'creator'", 'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '600', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cas_client.Subject']", 'null': 'True', 'blank': 'True'})
        },
        'cas_client.outcome': {
            'Meta': {'object_name': 'Outcome'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'departments': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cas_client.Department']", 'null': 'True', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '400'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'keywords': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cas_client.Keyword']", 'null': 'True', 'blank': 'True'}),
            'modules': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cas_client.Module']", 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'postrequisites'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cas_client.Outcome']"}),
            'subjects': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['cas_client.Subject']", 'null': 'True', 'blank': 'True'})
        },
        'cas_client.subject': {
            'Meta': {'object_name': 'Subject'},
            'creator': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['auth.User']"}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '1200', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '60'}),
            'number': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'prerequisites': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'postrequisites'", 'null': 'True', 'symmetrical': 'False', 'to': "orm['cas_client.Subject']"}),
            'term': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True', 'blank': 'True'}),
            'year': ('django.db.models.fields.CharField', [], {'max_length': '4', 'null': 'True', 'blank': 'True'})
        },
        'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['cas_client']